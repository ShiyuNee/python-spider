# encoding utf-8
import torch
from torch import nn
import torch.nn.functional as F
from transformers import BertTokenizer
from torch.optim import Adam
from torch.utils.data import DataLoader, Dataset
import argparse
import os
import tqdm

os.environ['CUDA_VISIBLE_DEVICES']='0'

def get_n_gram_data(data, n):
    res_data = []
    res_label = []
    if len(data) < n:
        raise VallueError("too short")
    start_idx = 0
    while start_idx + n <= len(data):
        res_data.append(data[start_idx: start_idx + n - 1])
        res_label.append(data[start_idx + n - 1])
        start_idx += 1
    return res_data, res_label

def get_data(path, n):
    res_data = []
    res_label = []
    tokenizer = BertTokenizer.from_pretrained('/users/nishiyu/ict/Models/bart-base-chinese')
    with open(path) as file:
        data = file.readlines()
        for sample in data:
            sample_data, sample_label = get_n_gram_data(tokenizer(sample, return_tensors='pt')['input_ids'][0], n)
            for idx in range(len(sample_data)):
                res_data.append(sample_data[idx])
                res_label.append(sample_label[idx])
    print('get data success!')
    return res_data, res_label

def get_args():
    parser = argparse.ArgumentParser()

    # 添加命令行参数
    parser.add_argument('--vocab_size', type=int, default=21128)
    parser.add_argument('--train_data', type=str)
    parser.add_argument('--test_data', type=str)
    parser.add_argument('--window_size', type=int)
    parser.add_argument('--epoch', type=int, default=50)
    parser.add_argument('--batch_size', type=int, default=4096)

    args = parser.parse_args()
    return args

class NGramDataset(Dataset):
    def __init__(self, data_path, window_size=3):
        self.data, self.label = get_data(data_path, window_size)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        return self.data[i], self.label[i]


class FeedForwardNNLM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, window_size, hidden_dim):
        # 单词嵌入E : 输入层 -> 嵌入层
        super(FeedForwardNNLM, self).__init__()
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        # 词嵌入层 -> 隐藏层
        self.e2h = nn.Linear((window_size - 1) * embedding_dim, hidden_dim)
        #  隐藏层 -> 输出层
        self.h2o = nn.Linear(hidden_dim, vocab_size)

        self.activate = F.relu

    def forward(self, inputs):
        embeds = self.embeddings(inputs).reshape([inputs.shape[0], -1])
        hidden = self.activate(self.e2h(embeds))
        output = self.h2o(hidden)
        
        return output


class Trainer():
    def __init__(self, args, embedding_dim, hidden_dim):
        self.args = args
        self.model = FeedForwardNNLM(self.args.vocab_size, embedding_dim, args.window_size, hidden_dim)
        self.train_dataset = NGramDataset(self.args.train_data, self.args.window_size)
        self.train_dataloader = DataLoader(self.train_dataset, batch_size=args.batch_size, shuffle=True)
        self.test_dataset = NGramDataset(self.args.test_data, self.args.window_size)
        self.test_dataloader = DataLoader(self.test_dataset, batch_size=args.batch_size, shuffle=False)

    def train(self):
        self.model.train()
        device = torch.device('cuda')
        self.model.to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = Adam(self.model.parameters(), lr=5e-6)
        for epoch in range(args.epoch):
            total_loss = 0.0
            for step, batch in enumerate(self.train_dataloader):
                input_ids = batch[0].to(device)
                label_ids = batch[1].to(device)
                logits = self.model(input_ids)
                loss = criterion(logits, label_ids)
                loss.backward()
                optimizer.step()
                self.model.zero_grad()

                total_loss += loss
            print(f'epoch: {epoch}, train loss: {total_loss / len(self.train_dataloader)}')
            self.evaluation()
            

    def evaluation(self):
        self.model.eval()
        device = torch.device('cuda')
        criterion = nn.CrossEntropyLoss()
        total_loss = 0.0
        for step, batch in enumerate(self.test_dataloader):
            input_ids = batch[0].to(device)
            label_ids = batch[1].to(device)
            logits = self.model(input_ids)
            loss = criterion(logits, label_ids)

            total_loss += loss
        print(f'eval loss: {total_loss / len(self.test_dataloader)}')

if __name__ == '__main__':
    args = get_args()
    trainer = Trainer(args, 128, 256)
    trainer.train()