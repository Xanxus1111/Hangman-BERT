import numpy as np
import os
def gen_q_a(word):
    answer = []
    question = []

    cur_word = word
    alphabet = list(set(list(word)))
    for k in range(len(alphabet)):
        cur_word = word
        for i in range(len(alphabet)):
            cur_word = cur_word.replace(alphabet[(i+k)%len(alphabet)],'_')
            question.append(cur_word)
            answer.append(alphabet[(i+k)%len(alphabet)])

    return question,answer

def get_dataPath(file_path='250k.txt',count = -1):
    all_q,all_a = [],[]
    

    root_path = file_path.split('/')[:-1]
    root_path = '/'.join(root_path)

    save_q_path = os.path.join(root_path,'all_q_{}.npy'.format(str(count)if count != -1 else ''))
    save_a_path = os.path.join(root_path,'all_a_{}.npy'.format(str(count)if count != -1 else ''))
    
    if os.path.exists(save_q_path) and os.path.exists(save_a_path):
        return save_q_path,save_a_path
        
    with open(file_path, 'r', encoding='utf-8') as f:
        words = f.readlines()
        for i, word in enumerate(words):
            word = word.strip()
            q,a = gen_q_a(word)
            all_q.extend(q)
            all_a.extend(a)
            if i == count:
                break
    print('-'*100)
    print(len(all_q))
    print(len(all_a))
    np.save(save_q_path,np.array(all_q))
    np.save(save_a_path,np.array(all_a))

    return 'all_q_{}.npy'.format(str(count)if count != -1 else ''), 'all_a_{}.npy'.format(str(count)if count != -1 else '')

if __name__== '__main__':
    get_dataPath('250k.txt',count=-1)