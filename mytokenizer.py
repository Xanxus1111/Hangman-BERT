
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
    