def kimchi_hash(str_obj):
    one_and_zeros = ""
    if str == '':
        return 1
    for i in str_obj:
        one_and_zeros += get_num(i)
    return int(one_and_zeros, 10)


alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


def get_num(s):
    if s in alpha:
        return str(alpha.index(s))
    if s in numbers:
        return str(numbers.index(s))
    return '0'
# TODO: cant use hash() in RPython
# arr = bytearray(str_obj)
# i = 0
# while i < len(arr):
#   one_and_zeros += str(format(arr[i]',' '08b')')
#   i+=1
# for i in bytearray(str_obj):
#     one_and_zeros += str(format(i, '08b'))
