from unittest import TestCase
from unittest.mock import patch
import re

from confuser.confuser_str import *
from confuser.confuser_params import params

class TestConfuserStr(TestCase):

    def test_delete_char( self ):
        assert delete_char('a') == ''
        assert delete_char('aa') == 'a'
        assert len(delete_char('aaabbb')) == 5
        assert delete_char('') == ''
        assert delete_char(None) == ''


    def test_insert_char( self ):
        assert len(insert_char('')) == 1
        assert len(insert_char(None)) == 1
        assert len(insert_char('aaabbb')) == 7


    def test_replace_char( self ):
        assert replace_char('') == ''
        assert replace_char(None) == ''
        assert replace_char('a') != 'a' or replace_char('a') != 'a'
        r = replace_char('aa')
        assert  r.startswith('a') or r.endswith('a')
        assert len(replace_char('aaabbb')) == 6
        assert replace_char('aaabbb') != 'aaabbb'


    def test_toggle_case_char( self ):
        assert toggle_case_char('') == ''
        assert toggle_case_char(None) == ''
        assert toggle_case_char('a') == 'A'
        assert toggle_case_char('A') == 'a'
        r = toggle_case_char('ab')
        assert  r.startswith('A') or r.endswith('B')
        o = 'abcdefghij'
        r = toggle_case_char(o)
        assert r != o
        assert r.lower() == o
        assert (len(re.findall('[A-Z]', r)) == 1)
        assert (len(re.findall('[a-z]', r)) == 9)
        o = 'ABCDEFGHIJ'
        r = toggle_case_char(o)
        assert (len(re.findall('[A-Z]', r)) == 9)
        assert (len(re.findall('[a-z]', r)) == 1)


    def test_transpose_chars( self ):
        assert transpose_chars('') == ''
        assert transpose_chars(None) == ''
        assert transpose_chars('a') == 'a'
        assert transpose_chars('ab') == 'ba'
        assert len(transpose_chars('abcdefghij')) == 10


    def test_duplicate_char( self ):
        assert duplicate_char('') == ''
        assert duplicate_char(None) == ''
        assert duplicate_char('a') == 'aa'
        d = duplicate_char('ab')
        assert  d == 'aab' or d == 'abb'
        assert len(duplicate_char('abcdefghij')) == 11

    def test_confuse_str_duplicate_char_branch( self ):
        with patch('confuser.confuser_str.random.random', side_effect=[0.0, 0.2]), \
             patch('confuser.confuser_str.random.randrange', return_value=1):
            original_max_typos = params.max_typos
            original_p_typo = params.p_typo
            original_p_del_char = params.p_del_char
            original_p_ins_char = params.p_ins_char
            original_p_rep_char = params.p_rep_char
            original_p_transp_char = params.p_transp_char
            original_p_dup_char = params.p_dup_char
            original_p_tog_case_char = params.p_tog_case_char
            try:
                params.max_typos = 1
                params.p_typo = 1.0
                params.p_del_char = 0.0
                params.p_ins_char = 0.0
                params.p_rep_char = 0.0
                params.p_transp_char = 0.0
                params.p_dup_char = 1.0
                params.p_tog_case_char = 0.0

                assert confuse_str('ab') == 'abb'
            finally:
                params.max_typos = original_max_typos
                params.p_typo = original_p_typo
                params.p_del_char = original_p_del_char
                params.p_ins_char = original_p_ins_char
                params.p_rep_char = original_p_rep_char
                params.p_transp_char = original_p_transp_char
                params.p_dup_char = original_p_dup_char
                params.p_tog_case_char = original_p_tog_case_char

    def test_get_obscure_str( self ):
        assert len(get_obscure_str()) == 10
        assert len(get_obscure_str(8)) == 8
        assert get_obscure_str() != get_obscure_str()
        assert re.search('[a-z]',get_obscure_str(10000)) != None
        assert re.search('[A-Z]',get_obscure_str(10000)) != None
        assert re.search('[0-9]',get_obscure_str(10000)) != None
