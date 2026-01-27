import random
import sys
import string
from .confuser_params import params


def delete_char( line ):

    if (line == None):
        return ''

    if (len(line) > 0):
        i = random.randrange(len(line))

        if (i == len(line)-1):
            line = line[:len(line)-1]
        else:
            line = line[:i] + line[i+1:]

    return line


def insert_char( line ):

    c = random.choice(string.ascii_letters)

    if (line == None or line == ''):
        return c

    i = random.randrange(len(line))

    line = line[:i] + c + line[i:]

    return line


def replace_char( line ):

    if (line == None):
        return ''

    if (len(line) > 0):
        i = random.randrange(len(line))
        c = random.choice(string.ascii_letters)

        line = line[:i] + c + line[i+1:]
        
    return line


def toggle_case_char( line ):

    if (line == None):
        return ''

    if (len(line) > 0):
        i = random.randrange(len(line))

        line = line[:i] + line[i].swapcase() + line[i+1:]

    return line


def transpose_chars( line ):

    if (line == None):
        return ''

    if (len(line) > 1):
        i = random.randrange(len(line)-1)
        line = line[:i] + line[i+1:i+2] + line[i:i+1] + line[i+2:]
        
    return line

def duplicate_char( line ):

    if (line == None):
        return ''

    if (len(line) > 0):
        i = random.randrange(len(line))
        line = line[:i] + line[i] + line[i:]

    return line



def confuse_str( line ):

    line = line.strip()
    for errorcount in range(0,params.max_typos):
        if (random.random() < params.p_typo):
            # line needs to be mutated
            r = random.random()

            if (r > 1 - params.p_del_char):
                # delete a rand caharacter
                line = delete_char(line);

            elif (r > 1 - params.p_del_char - params.p_ins_char):
                # insert a rand character
                line = insert_char(line);

            elif (r > 1 - params.p_del_char - params.p_ins_char - params.p_rep_char):
                # replace a rand character by another rand character
                line = replace_char(line);

            elif (r > 1 - params.p_del_char - params.p_ins_char - params.p_rep_char - params.p_transp_char):
                # replace a rand character by another rand character
                line = transpose_chars(line);

            elif (r > 1 - params.p_del_char - params.p_ins_char - params.p_rep_char - params.p_transp_char - params.p_dup_char):
                # replace a rand character by another rand character
                line = transpose_chars(line);

            elif (r > 1 - params.p_del_char - params.p_ins_char - params.p_rep_char - params.p_transp_char - params.p_dup_char - params.p_tog_case_char):
                # capitalise a rand character 
                line = toggle_case_char(line);

    return line

def get_obscure_str( i = 10 ):
    return ''.join(random.choices(string.digits + string.ascii_letters, k = i))

