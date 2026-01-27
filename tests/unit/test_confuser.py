from unittest import TestCase
from confuser.confuser import *
from confuser.confuser_schema import resolver
import copy
import os


class TestConfuser(TestCase):

    def test_get_new_writer( self ):
        nw = get_new_writer('./', 'file.csv', { 'col1': 1, 'col2': None })
        assert os.access('./' + resolver.obscure_name('file.csv'), os.W_OK)
        os.unlink('./' + resolver.obscure_name('file.csv'))

    def test_switch_table( self ):
        nw = switch_table('./', 'file.csv', { 'col1': None, 'col2': [] }, 10)
        print(resolver.name2obs)
        assert os.access('./' + resolver.obscure_name('file_10.csv'), os.W_OK)
        os.unlink('./' + resolver.obscure_name('file_10.csv'))
        nw = switch_table('./', 'file', { 'col1': {}, 'col2': None }, 5)
        assert os.access('./' + resolver.obscure_name('file_5.csv'), os.W_OK)
        os.unlink('./'+resolver.obscure_name('file_5.csv'))

    def test_mutate_descriptions( self ):
        m = mutate_descriptions({ 'col1': 1, 'col2_DESCRIPTION': 'abcdef', 'col3': '3' })
        assert m[resolver.obscure_name('col1')] == 1
        assert m[resolver.obscure_name('col3')] == '3'
        assert m[resolver.obscure_name('col2_DESCRIPTION')] != 'abcdef'

    def test_misplace_row( self ):
        pass 

    def test_drop_row( self ):
        assert drop_row('') == None
        assert drop_row(None) == None
        assert drop_row('abcdef') == None
        assert drop_row('three little pigs') == None

    def test_drop_value( self ):
        assert drop_value({'a':3}) == {'a':'NULL'}
        assert drop_value({}) == {}
        e = {'a':1,'b':2,'c':3}
        d = drop_value(copy.deepcopy(e))
        assert d != e
        assert d == {'a':'NULL','b':2,'c':3} or d == {'a':1,'b':'NULL','c':3} or d == {'a':1,'b':2,'c':'NULL'}

    def test_dup_row( self ):
        assert dup_row('') == '\n'
        assert dup_row(None) == '\n'
        assert dup_row('abcdef') == 'abcdef\nabcdef'
        assert dup_row('three little pigs') == 'three little pigs\nthree little pigs'
