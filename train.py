import numpy as np
from torch.utils.data import Dataset
import torch

from torch.utils.data import DataLoader
# from transformers import AdamW
from torch.optim import AdamW
from transformers import BertConfig, BertForSequenceClassification
from mytokenizer import MyTokenizer
from dataset.gendata import get_dataPath
import time
np.random.seed(42)
torch.manual_seed(42)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(42)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


vocab_file_dir = './vocab.txt'

tokenizer = MyTokenizer(vocab_file_dir)
print(tokenizer.get_vocab_size())
print(tokenizer.vocab)

class HangmanDataset(Dataset):
    def __init__(self, question, answer, tokenizer,max_length):
        self.tokenizer = tokenizer
        self.inputs = []
        self.targets = []

        for q,a in zip(question, answer):
            encoding = tokenizer.encode(q)
            encoding = tokenizer.pad(encoding,max_length)
            self.inputs.append(encoding)
            self.targets.append([ord(a) - ord('a')])
    
    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return torch.tensor(self.inputs[idx], dtype=torch.long), torch.tensor(self.targets[idx], dtype=torch.long)


# gen data
data_path = './dataset/250k.txt'
q_path,a_path = get_dataPath(file_path = data_path,count = -1)
question = np.load(q_path)
answer = np.load(a_path).tolist()

# 统计最大长度
max_length = max(len(q) for q in question) + 2
print('单词最大长度',max_length)
question = question.tolist()

# 创建一个新的配置
config = {
    "vocab_size": tokenizer.get_vocab_size(),
    "hidden_size": 256,
    "num_hidden_layers": 2,
    "num_attention_heads": 4,
    "intermediate_size": 1024,
    "hidden_act": "gelu",
    "hidden_dropout_prob": 0.1,
    "attention_probs_dropout_prob": 0.1,
    "max_position_embeddings": max_length,
    "type_vocab_size": 1,
    "initializer_range": 0.02,
    "layer_norm_eps": 1e-12,
    "num_labels": 26
}
config =BertConfig(**config)
model = BertForSequenceClassification(config)

dataset = HangmanDataset(question,answer, tokenizer,max_length)
# dataloader = DataLoader(dataset, batch_size=4096,shuffle=True,num_workers=25) 
dataloader = DataLoader(dataset, batch_size=12288,shuffle=True,num_workers=25) 


# optimizer = AdamW(model.parameters(), lr=1e-3)
optimizer = AdamW(model.parameters(), lr=3e-3)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, 10, eta_min=1e-6)


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)

epoch = 1
# from tqdm import tqdm
# for epoch in tqdm(range(epoch), desc="outer_loop"):
#     for batch in tqdm(dataloader, desc="inner_loop", leave=False):
st_time = time.time()
for epoch in range(epoch):
    for b,batch in enumerate(dataloader):
        inputs, targets = batch
        inputs = inputs.to(device)
        targets = targets.to(device)
        # if epoch == 0:
        #     print(inputs[0],targets[0],tokenizer.decode(inputs[0].tolist()),':',chr(targets[0] + ord('a')))
        outputs = model(inputs, labels=targets)
        loss = outputs.loss
        if b % 100 == 0:
            print('loss',loss.item(),'lr',optimizer.param_groups[0]['lr'])
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        scheduler.step()
    # save model
    model.save_pretrained("my_model_all_{}".format(epoch))

print('time',time.time() - st_time)


