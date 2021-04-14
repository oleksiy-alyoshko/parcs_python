import numpy as np

mx = 1000

n_row = np.random.choice(range(500,1000))
n_col = np.random.choice(range(500,1000))
matrix = []
vector = []
for i in range(n_row):
    row = []
    for j in range(n_col):
        row.append(np.random.choice(range(mx)))
        if i == 0:
            vector.append(np.random.choice(range(mx)))
    matrix.append(row)

with open('input_1500_3500.txt', 'w') as f:
    f.write('{} {}\n'.format(n_row, n_col))
    for i in range(n_row):
        for j in range(n_col):
            f.write('{} '.format(matrix[i][j]))
        f.write('\n')
    for j in range(n_col):
        f.write('{}\n'.format(vector[j]))
