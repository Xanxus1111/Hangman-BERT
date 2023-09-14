import random


class Game():
    '''
    '''
    def __init__(self,word_len_range = [4,16],wrong_guess = 7):
        self.failer = 0
        # 读取数据
        self.word_list = []
        self.wrong_guess = wrong_guess
        # with open('dataset/250k.txt', 'r') as f:
        with open('dataset/20k.txt', 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if  word_len_range[0] < len(line) < word_len_range[1]:
                    self.word_list.append(line)
        
        self.guess_wrong_count = 0

        self.word = ''
        self.alraedy_guess = []

    def run(self,alphabet = ''):
        if alphabet == '':
            #随机选择一个单词
            self.reset()
            self.word = self.select_word()
            self.should_guess_word = list(set(list(self.word)))

        #处理后，返回给用户
        res = self.process(alphabet)
        if res == 'N':
            return -1
        else:
            return res

    def select_word(self):
        return random.choice(self.word_list)

    def get_word(self):
        newword = self.word
        for each in self.should_guess_word:
            newword = newword.replace(each, '_')
        return newword

    def process(self, alphabet=''):
        if alphabet == '':
            newword = '_' * len(self.word)
            return newword
        else:
            if alphabet not in self.alraedy_guess:
                self.alraedy_guess.append(alphabet)
                if alphabet in self.word:
                    self.should_guess_word.remove(alphabet)
                    if len(self.should_guess_word) == 0:
                        return 1
                    return self.get_word()
                else:
                    self.failer += 1
                    print('wrong guess', self.failer)
                    if self.failer == self.wrong_guess:
                        print('you loss, answer is:', self.word)
                        return 'N'
                    else:
                        return self.get_word()
                        
            else:
                return self.get_word()

    def reset(self):
        self.word = ''
        self.should_guess_word = []
        self.guess_wrong_count = 0
        self.alraedy_guess = []
        self.failer = 0