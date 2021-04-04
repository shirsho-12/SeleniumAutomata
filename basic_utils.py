from bs4 import BeautifulSoup


def get_folder_name(line):
    line = line.split('-').pop()
    return '/' + line[1:]


def make_soup(text):
    return BeautifulSoup(text, 'html.parser')


def name_func(name):
    translation_table = str.maketrans({':': '-', ">": ' ', "<": " ",
                                       '"': ' ', '/': ' ',
                                       '|': ' ', '?': ' ', '*': ' '})
    # import string
    # table_2 = str.maketrans( string.punctuation, ' ' * len(string.punctuation))
    name = name.translate(translation_table)
    return '/' + name
    # return '/David Chalmers- The Hard Problem of Consciousness.mp3'


"""
def lcs(str_1, str_2):
    """ """
    Gets the LCS( Longest Common Substring of 2 strings
    Determines the name of the folder
    Parameters:
          str_1: string
          str_2: string
    :returns lcs_val: int stating length of the LCS
    """ """
    len_str_1, len_str_2 = len(str_1), len(str_2)

    dp_arr = [[0] * (len_str_2 + 1) for i in range(len_str_1 + 1)]
    for i in range(1, len_str_1 + 1):
        for j in range(1, len_str_2 + 1):
            if str_1[i - 1] == str_2[j - 1]:
                dp_arr[i][j] = dp_arr[i - 1][j - 1] + 1
            else:
                dp_arr[i][j] = max(dp_arr[i - 1][j], dp_arr[i][j - 1])

    lcs_val = dp_arr[len_str_1][len_str_2]
    return lcs_val

Deprecated for easier (more error-prone to multiple hyphens) approach
def get_folder_name(data_array):
    # Function to determine folder name using LCS (Largest Common Substring)
    size = len(data_array)
    line = data_array[random.randint(0, size - 1)][1]
    val = lcs(line , data_array[random.randint(0, size - 1)][1])
    return '/' + line[-val:]
"""
