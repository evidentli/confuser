from unittest import TestCase
from unittest.mock import patch
from confuser.confuser import *
from confuser.confuser_schema import resolver
import copy
import csv
import os


class TestConfuser(TestCase):

    def test_get_new_writer( self ):
        nw = get_new_writer('./', 'nested/file.csv', { 'col1': 1, 'col2': None })
        assert os.access('./' + resolver.obscure_name('file.csv'), os.W_OK)
        nw.close()
        os.unlink('./' + resolver.obscure_name('file.csv'))

    def test_switch_table( self ):
        nw = switch_table('./', 'file.csv', { 'col1': None, 'col2': [] }, 10)
        print(resolver.name2obs)
        assert os.access('./' + resolver.obscure_name('file_10.csv'), os.W_OK)
        nw.close()
        os.unlink('./' + resolver.obscure_name('file_10.csv'))
        nw = switch_table('./', 'file', { 'col1': {}, 'col2': None }, 5)
        assert os.access('./' + resolver.obscure_name('file_5.csv'), os.W_OK)
        nw.close()
        os.unlink('./'+resolver.obscure_name('file_5.csv'))

    def test_mutate_descriptions( self ):
        m = mutate_descriptions({ 'col1': 1, 'col2_DESCRIPTION': 'abcdef', 'col3': '3' })
        assert m[resolver.obscure_name('col1')] == 1
        assert m[resolver.obscure_name('col3')] == '3'
        assert m[resolver.obscure_name('col2_DESCRIPTION')] != 'abcdef'

    def test_mutate_descriptions_lowercase_header( self ):
        m = mutate_descriptions({ 'description': 'abcdef', 'patient': '123' })
        assert m[resolver.obscure_name('patient')] == '123'
        assert m[resolver.obscure_name('description')] != 'abcdef'

    def test_mutate_descriptions_numbered_headers( self ):
        m = mutate_descriptions({ 'description1': 'abcdef', 'reasonDescription2': 'ghijkl', 'patient': '123' })
        assert m[resolver.obscure_name('patient')] == '123'
        assert m[resolver.obscure_name('description1')] != 'abcdef'
        assert m[resolver.obscure_name('reasonDescription2')] != 'ghijkl'

    def test_mutate_descriptions_with_literal_quoted_headers( self ):
        row = {'"DESCRIPTION"': 'primary', '"DESCRIPTION1"': 'secondary', '"PATIENT"': 'id'}
        with patch('confuser.confuser.confuse_str', side_effect=lambda line: f'{line}!'):
            result = mutate_descriptions(row)

        assert result[resolver.obscure_name('"DESCRIPTION"')] == 'primary!'
        assert result[resolver.obscure_name('"DESCRIPTION1"')] == 'secondary!'
        assert result[resolver.obscure_name('"PATIENT"')] == 'id'

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
        assert dup_row('') == True
        assert dup_row(None) == False
        assert dup_row('abcdef') == True
        assert dup_row('three little pigs') == True

    def test_confuse_handles_quoted_headers( self ):
        in_dir = './tmp_quoted_headers_in'
        out_dir = './tmp_quoted_headers_out'
        in_file = os.path.join(in_dir, 'allergies.csv')

        os.mkdir(in_dir)
        os.mkdir(out_dir)

        with open(in_file, 'w', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(['start', 'stop', 'patient'])
            writer.writerow(['1988-01-07', '', 'abc-123'])

        try:
            confuse(seed=123, in_path=in_dir, out_path=out_dir, verbose=False)

            out_files = os.listdir(out_dir)
            assert len(out_files) >= 1

            out_file = os.path.join(out_dir, out_files[0])
            with open(out_file, 'r', newline='') as f:
                rows = list(csv.DictReader(f))

            assert len(rows) == 1
            assert rows[0]
            assert 'abc-123' in rows[0].values()
        finally:
            if os.path.exists(in_file):
                os.unlink(in_file)
            if os.path.isdir(in_dir):
                os.rmdir(in_dir)

            for out_file in os.listdir(out_dir) if os.path.isdir(out_dir) else []:
                os.unlink(os.path.join(out_dir, out_file))
            if os.path.isdir(out_dir):
                os.rmdir(out_dir)
