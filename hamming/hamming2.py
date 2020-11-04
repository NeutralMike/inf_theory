import numpy as np

with open('input.txt', 'r') as input_file, open('output.txt', 'w') as output_file:
    words = input_file.read().split()
    r = int(np.ceil(np.log2(len(words[0])))) + 1
    n = 2**r - 1
    k = n - r
    print(r, n, k)

    words = np.array(list(map(list, words))).astype('uint8')
    H = np.empty((r, 1), dtype='uint8')
    words_count = words.shape[0]

    # fill check matrix
    for i in range(n+1):
        H = np.hstack((H, np.array([(i >> j) & 1 for j in range(r-1, -1, -1)]).reshape((r, 1))))
    words = np.concatenate((words, np.zeros((words_count, k - words.shape[1]), dtype='uint8')), axis=1)

    H = H[:, 2:]
    A = np.delete(H, 2**np.arange(r)-1, axis=1)
    H = np.concatenate((A, np.eye(n-k, dtype='uint8')), axis=1)
    print(H)
    G = np.concatenate((np.eye(k, dtype='uint8'), -A.T % 2), axis=1)
    print(G)

    coded_words = (words @ G) % 2

    # generate error (reverse) of random bit in every word
    errors_real = np.random.randint(n, size=words_count)
    for i in range(words_count):
        coded_words[i, errors_real[i]-1] = (coded_words[i, errors_real[i]-1] + 1) % 2

    # check for errors
    errors = (H @ coded_words.T) % 2

    # convert bit matrix of error to numbers of bit
    founded_errors = []
    for i in range(words_count):
        founded_errors.append((2**np.arange(r))[::-1][errors[:, i] == 1].sum())
    founded_errors = np.array(founded_errors)

    print('Real errors:', errors_real)
    print('Founded errors:', founded_errors)
    print('Every error is founded correct:', np.allclose(np.array(errors_real), np.array(founded_errors)))
