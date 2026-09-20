from unittest import TestCase
from confuser.confuser_split_writer import *

class TestConfuserDate(TestCase):

    def test_split_wrtier( self ):
        a = split_writer(['a', 'b', 'c', 'd', 'e'], './table.csv')
        a.writeheader()
        a.writerow({'a': 1, 'b':2, 'c':3, 'd':4, 'e':5})

        assert os.access('./a_table.csv', os.R_OK)
        assert os.access('./b_table.csv', os.R_OK)
        with open('./a_table.csv', 'r') as f:
            ahead = f.readline()
            print("ahead: ", ahead)
            abody = f.readline()
            print("abody: ", abody)

        with open('./a_table.csv', 'r') as f:
            alines = f.readlines()
            print(alines)

        with open('./b_table.csv', 'r') as f:
            bhead = f.readline()
            bbody = f.readline()

        assert ahead.startswith('a')
        assert bhead.startswith('a')
        assert sum(1 for x in ahead if x == ',') == 2
        assert sum(1 for x in abody if x == ',') == 2
        assert sum(1 for x in bhead if x == ',') == 2
        assert sum(1 for x in bbody if x == ',') == 2

        a.close()
        os.unlink('./a_table.csv')
        os.unlink('./b_table.csv')
