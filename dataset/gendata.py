import numpy as np

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
    # file_path = '20k.txt'
    all_q,all_a = [],[]
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
    np.save('all_q_{}.npy'.format(str(count)if count != -1 else ''),np.array(all_q))
    np.save('all_a_{}.npy'.format(str(count)if count != -1 else ''),np.array(all_a))

    return 'all_q_{}.npy'.format(str(count)if count != -1 else ''), 'all_a_{}.npy'.format(str(count)if count != -1 else '')

