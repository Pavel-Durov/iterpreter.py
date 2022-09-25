def kimchi_hash(str_obj):
    """
    This function is kind of weird.
    Main reason for this function is to convert a string to a number
    The problem is that we cant use hash() in RPython :(
    """
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
