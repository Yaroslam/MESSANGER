from random import randint

def encode(symbol):
    m = 3
    matrix = [[randint(0,100) for x in range(m)] for y in range(m)]
    matrix[m-1][2] = 0
    matrix[m-1][2] = calculate_last(matrix, symbol)
    encode_arr = []
    for i in range(m):
        for j in range(m):
            encode_arr.append(matrix[i][j])
    return encode_arr


def decode(encode_arr):
    m = 3
    decode_matr = [[0 for x in range(m)] for y in range(m)]
    for i in range(m):
        for j in range(m):
            decode_matr[i][j] = encode_arr[i*m+j]
    return get_det(decode_matr)


def calculate_last(matrix, symbol):
    det = ord(symbol)
    remain_of_det = det - matrix[0][1]*matrix[1][2]*matrix[2][0] - matrix[0][2]*matrix[1][0]*matrix[2][1]+\
                matrix[0][2]*matrix[1][1]*matrix[2][0] + matrix[0][0]*matrix[1][2]*matrix[2][1]

    return remain_of_det/(matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0])


def get_det(matrix):
    return  matrix[0][1] * matrix[1][2] * matrix[2][0] + matrix[0][2] * matrix[1][0] * matrix[2][1] -\
    matrix[0][2] * matrix[1][1] * matrix[2][0] - matrix[0][0] * matrix[1][2] * matrix[2][1] - matrix[0][1]*matrix[1][0]* matrix[2][2] + \
          matrix[0][0]*matrix[1][1]*matrix[2][2]
