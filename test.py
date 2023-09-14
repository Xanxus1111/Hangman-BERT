from game import Game
from infer import hangmanAgent

import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('please input mode')
        exit()
    mode = sys.argv[1]

    game = Game()
    lose_count = 0  
    win_count = 0
    flag = 'start'
    total = game_time = 1000
    alphabet = ''

    if mode == 'h':
        while True:
            if game_time == 0:
                break
            res = game.run(alphabet)
            if res == -1:
                lose_count += 1
                game_time -= 1
                alphabet = ''
            elif res == 1 :
                print('win')
                game_time -= 1
                alphabet = ''
                win_count += 1
            else:
                print(res)
                alphabet = input('input a alphabet:')
    elif mode == 'ai':
        agent = hangmanAgent()
        while True:
            if game_time == 0:
                break
            res = game.run(alphabet)
            if res == -1:
                lose_count += 1
                game_time -= 1
                alphabet = ''
                agent.guess('N')
            elif res == 1 :
                print('win')
                game_time -= 1
                alphabet = ''
                agent.guess('N')
                win_count += 1
            else:
                print('game: ',res)
                alphabet = agent.guess(res)
        
        print('success rate:',round((win_count)/total,2),'lose: ',lose_count,'total: ',total)
    else:
        print('wrong mode')