import numpy as np


word = input("Enter word: ").strip()
n = len(word)
word = np.array(list(word)).astype(np.int8)
order = np.arange(n+1)+1
mask = np.where(word == 1)
if (order[mask]).sum() % (n+1) == 0:
    print("Word is correct")
else:
    print("Wrong word")
    exit()

choise = input("1) insert bit\n2) drop bit\n")
if choise == '1':
    print(word)
    k = int(input("enter number from %d to %d for insert: " % (1, n+1)))
    new_bit = int(input("insert 0 or 1 ?: "))
    word = np.insert(word, k-1, new_bit)
    mask = np.where(word == 1)
    print(word)
    T = (order[mask]).sum() % (n+1)
    count_k = n
    if T == 0:
        count_k = n
    elif T == word.sum():
        count_k = 0
    elif T < word.sum():
            count_k = np.where(word == 1)[0][-T]-1
    elif T > word.sum():
        count_k = np.where(word == 0)[0][-(n + 1 - T)]-1
    word = np.delete(word, count_k)
    print(word)
if choise == '2':
    print(word)
    k = int(input("enter number from %d to %d for drop: " % (1, n)))
    word = np.delete(word, k-1)
    print(word)
    mask = np.where(word == 1)
    T = -(order[mask]).sum() % (n+1)
    if word.sum() >= T:
        count_k = np.where(word == 1)[0][-T]
        word = np.insert(word, count_k, 0)
    else:
        if n-T == 0:
            word = np.insert(word, n-1, 1)
        else:
            count_k = np.where(word == 0)[0][-(n - T)]
            word = np.insert(word, count_k, 1)
    print(word)


