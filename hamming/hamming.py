import numpy as np

with open('input.txt', 'r') as input_file, open('output.txt', 'w') as output_file:
    words = input_file.read().split()
    r = int(np.ceil(np.log2(len(words[0]))))+1
    n = 2**r - 1
    k = n - r
    print(r, n, k)

    words = np.array(list(map(list, words))).astype('uint8')
    check_matrix = np.empty((r, 1), dtype='uint8')
    words_count = words.shape[0]

    # fill check matrix
    for i in range(n+1):
        check_matrix = np.hstack((check_matrix, np.array([(i >> j) & 1 for j in range(r-1, -1, -1)]).reshape((r, 1))))
    check_matrix = check_matrix[:, 2:]
    print(check_matrix, '\n')

    # add bits to words, so they k-long
    words = np.concatenate((words, np.zeros((words_count, k - words.shape[1]), dtype='uint8')), axis=1)

    # add r check bits to words< so they n-long
    coded_words = np.insert(words, 2**np.arange(r)-1 - np.arange(r), np.zeros((words_count, r), dtype='uint8'), axis=1)

    # compute check bits by matmul on check matrix
    coded_words[:, 2**np.arange(r)-1] = (coded_words @ check_matrix[-1::-1].T) % 2
    print(coded_words, '\n')

    # generate error (reverse) of random bit in every word
    errors_real = np.random.randint(n, size=words_count)
    for i in range(words_count):
        coded_words[i, errors_real[i]-1] = (coded_words[i, errors_real[i]-1] + 1) % 2

    # check for errors
    errors = (check_matrix @ coded_words.T) % 2

    # convert bit matrix of error to numbers of bit
    founded_errors = []
    for i in range(words_count):
        founded_errors.append((2**np.arange(r))[::-1][errors[:, i] == 1].sum())

    print('Real errors:', errors_real)
    print('Founded errors:', founded_errors)
    print('Every error is founded correct:', np.allclose(np.array(errors_real), np.array(founded_errors)))
