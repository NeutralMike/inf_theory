import numpy as np
import math
from pyfinite import ffield
from random import random, randint


# message = list(map(int, input('Enter separated numbers: ').split()))
# t = int(input('How much loss numbers should be restored? '))
# k = len(message)
# n = t * 2 + k

def div_mod(message, gen):
    temp_str = ''
    for i in range(len(message)):
        temp_str += message[i]
        temp_str = temp_str.lstrip('0')
        if len(temp_str) == len(bin(gen)) - 2:
            temp_str = bin(int(temp_str, 2) ^ gen)[2:]
    return temp_str

degree = 4
n = 15
k = 11
t = math.floor((n-k)/2)
message = int('01101011011', 2)
zeros_at_start = k - len(bin(message)) + 2
message = message << (n-k)

gf = ffield.FField(degree)
message_str = '0' * zeros_at_start + bin(message)[2:]
print('message:          ', message_str)

generator_values_str = div_mod(message_str, gf.generator)
message_str = message_str[:k] + generator_values_str
corrupt_ind = randint(0, k+1)
corrupted_message = ''
if message_str[corrupt_ind] == '0':
    corrupted_message = message_str[:corrupt_ind] + '1' + message_str[corrupt_ind+1:]
else:
    corrupted_message = message_str[:corrupt_ind] + '0' + message_str[corrupt_ind + 1:]
err_gf = div_mod(corrupted_message, gf.generator)
print('corrupted message:', corrupted_message)
for i in range(n):
    if err_gf == div_mod(bin(2**i)[2:], gf.generator):
        print('Ошибвка в %d бите с конца' % (i+1))
# message = np.append(np.array(message), np.full(n-k, 0)).reshape((-1, 1))

# print('corrupted_message:', ''.join(map(str, corrupted_message)))


