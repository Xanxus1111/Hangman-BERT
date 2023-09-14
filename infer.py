
import torch
from transformers import  BertForSequenceClassification
from mytokenizer import MyTokenizer

class MyTokenizer():
    def __init__(self, vocab_file_dir = './vocab.txt'):
        with open(vocab_file_dir, 'r') as f:
            self.vocab = f.readlines()
            self.vocab = [i.strip() for i in self.vocab]
            self.vocab = {i:idx for idx,i in enumerate(self.vocab)}
            self.token2vocab = {idx:i for idx,i in enumerate(self.vocab)}
    
    def get_vocab_size(self):
        return len(self.vocab)
    
    def encode(self,word):
        word = word.strip()
        return [self.vocab[i] for i in word]
    
    def decode(self,tokens):
        return [self.token2vocab[i] for i in tokens]

    def encode_target(self,word):
        word = word.strip()
        return [self.vocab[i] for i in word]
    
    def decode_target(self,tokens):
        return [self.token2vocab[i] for i in tokens]

    def pad(self,token,max_length):
        return [self.vocab['[CLS]']] + token + [self.vocab['[PAD]']]*(max_length-len(token)-2) + [self.vocab['[SEP]']]
    
class hangmanAgent():
    def __init__(self,vocab_file_dir = './vocab.txt',model_dir = './my_19'):
        self.vocab_file_dir = vocab_file_dir
        self.tokenizer = MyTokenizer(self.vocab_file_dir)
        self.model = BertForSequenceClassification.from_pretrained(model_dir)
        # 使用模型进行推断
        self.model.eval()

        self.max_length = 31

        self.pre_input = ''
        self.index = 0
        self.gus_list = []

    
    def guess(self,single_word):
        tokenizer = self.tokenizer
        if  single_word == 'N' or ('_' not in single_word and len(single_word) > 1):
            self.pre_input = ''
            self.index = 0
            self.gus_list = []
            if ('_' not in single_word and len(single_word) > 1):
                print('AI: win')
            return ''
        if single_word == 'R':
            single_word = self.pre_input
    
        for s in single_word:
            if s != '_':
                self.gus_list.append(s)
                self.gus_list = list(set(self.gus_list))
    
        encoding = [tokenizer.encode(single_word)]
        inputs = [tokenizer.pad(q,self.max_length) for q in encoding]
        inputs = torch.tensor(inputs)
        with torch.no_grad():
            outputs = self.model(inputs)
    
        # 按照概率 排序 获得索引值,逆序
        predictions = outputs.logits.argsort(dim=-1,descending=True)
        each = predictions[0]
        # print('argsort',predictions)
        if self.pre_input == single_word :
            while chr(each[self.index].item() + ord('a')) in self.gus_list:
            #select another label
                self.index +=1
        
        else:
            self.index = 0
            while chr(each[self.index].item() + ord('a')) in self.gus_list:
            #select another label
                self.index +=1
        self.gus_list.append(chr(each[self.index].item() + ord('a')))
        
        print('AI: ',single_word,'index:',self.index,chr(each[self.index].item() + ord('a')))
        print('AI: ',self.gus_list )
        self.pre_input = single_word
        return chr(each[self.index].item() + ord('a'))
if __name__ == '__main__':

    hmA = hangmanAgent()
    while True:
        word = input('input a word:')
        hmA.guess(word)
    




