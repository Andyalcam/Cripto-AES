from expansionLlaves import *
from cifrado import *

inv_sbox = [
		[0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
		[0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
		[0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
		[0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
		[0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
		[0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
		[0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
		[0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
		[0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
		[0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
		[0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
		[0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
		[0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
		[0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
		[0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
		[0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
]

def inv_sub_bytes(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            value = state[i][j] % 256  # Nos aseguramos de que el valor esté en el rango 0-255
            state[i][j] = inv_sbox[value // 0x10][value % 0x10]
    return state

def inv_shift_rows(state):
    state[0][1], state[1][1], state[2][1], state[3][1] = \
        state[1][1], state[2][1], state[3][1], state[0][1]
    state[0][2], state[1][2], state[2][2], state[3][2] = \
        state[2][2], state[3][2], state[0][2], state[1][2]
    state[0][3], state[1][3], state[2][3], state[3][3] = \
        state[3][3], state[0][3], state[1][3], state[2][3]
    return state

def inv_mix_columns(state):
    for j in range(4):
        s0 = state[j][0]
        s1 = state[j][1]
        s2 = state[j][2]
        s3 = state[j][3]

        state[j][0] = (GF_MUL_2[s0] ^ GF_MUL_2[s1] ^ s2 ^ s3)
        state[j][1] = (s0 ^ GF_MUL_2[s1] ^ GF_MUL_2[s2] ^ s3)
        state[j][2] = (s0 ^ s1 ^ GF_MUL_2[s2] ^ GF_MUL_2[s3])
        state[j][3] = (GF_MUL_2[s0] ^ s1 ^ s2 ^ GF_MUL_2[s3])
    return state

def decipher(ciphertext, key):
    Nr = 10
    Nb = 4
    print("round[10].output       ", ciphertext)
    state = str_to_matrix(ciphertext)
    key_schedule = keyExpansion(key)

    state = add_round_key(state, key_schedule[4*Nr:4*Nr+4])
    print("round[10].k_sch\t\t{}".format(matrix_to_str(state)))
    
    for round in range(Nr - 1, 0, -1):
        state = inv_shift_rows(state)
        print("round[ {}].s_row\t\t{}".format(round, matrix_to_str(state)))
        state = inv_sub_bytes(state)
        print("round[ {}].s_box\t\t{}".format(round, matrix_to_str(state)))
        state = add_round_key(state, key_schedule[4*round:4*round+4])
        print("round[ {}].k_sch\t\t{}".format(round, matrix_to_str(state)))
        state = inv_mix_columns(state)
        print("round[ {}].m_col\t\t{}".format(round, matrix_to_str(state)))

    state = inv_shift_rows(state)
    print("round[i].s_row\t\t{}".format(matrix_to_str(state)))
    state = inv_sub_bytes(state)
    print("round[i].s_box\t\t{}".format(matrix_to_str(state)))
    state = add_round_key(state, key_schedule[0:4])
    print("round[i].k_sch\t\t{}".format(matrix_to_str(state)))
    
    return matrix_to_str(state)

# Función auxiliar para convertir un string hexadecimal a una matriz
def str_to_matrix(hex_string):
    matrix = []
    for i in range(0, len(hex_string), 2):
        byte = int(hex_string[i:i + 2], 16)
        if len(matrix) < 4:
            matrix.append([byte])
        else:
            matrix[i // 2 % 4].append(byte)
    return matrix

# Función auxiliar para convertir una matriz a un string hexadecimal
def matrix_to_str(matrix):
    hex_string = ""
    for i in range(4):
        for j in range(4):
            hex_string += format(matrix[j][i], '02x')
    return hex_string

# Polinomios de multiplicación para inv_mix_columns
GF_MUL_2 = [0]*256
for i in range(256):
    GF_MUL_2[i] = (i << 1) ^ (0x1b if (i & 0x80) else 0)

# Aplicar las funciones a ciphertext y key
ciphertext = "3925841d02dc09fbdc118597196a0b32"
key = ["2b", "7e", "15", "16", "28", "ae", "d2", "a6", "ab", "f7", "15", "88", "09", "cf", "4f", "3c"]

print("\nProceso de descifrado")
print("PLAINTEXT:\t       ", decipher(ciphertext, key))