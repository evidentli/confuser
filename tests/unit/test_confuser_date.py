from unittest import TestCase
import re

from confuser.confuser_date import *

class TestConfuserDate(TestCase):

    def test_is_date( self ):
        assert is_date('2010-04-21') == True
        assert is_date('1') == False
        assert is_date('') == False
        assert is_date('a') == False
        assert is_date('1977-13-13') == False
        assert is_date(None) == False
        assert is_date('21.4.2022') == True
        assert is_date('2010-04-21T00:00:00') == True
        assert is_date('2010-04-21 13:33:55') == True
        assert is_date('11:33:55 2010-04-21') == True
        assert is_date('11:33 21/4/2010') == True
        assert is_date('123103810283010') == False

    def test_dates( self ):
        assert dates({'L':'2010-04-21','E':'2007-11-14','D':'2003-10-09','N':'1975-06-01','G':'1974-01-13','R':'1942-06-21','A':'1940-09-07'}) == ['L','E','D','N','G','R','A']
        assert dates({'L':'nil','E':'2007-11-14','D':'2003-10-09','N':'1975-06-01','G':'1974-01-13','R':'1942-06-21','A':'1940-09-07'}) == ['E','D','N','G','R','A']
        assert dates(['none','blah','foo','bar']) == []
        assert dates([]) == []
        assert dates(None) == []
        assert dates('this is a string') == []
        assert dates(1231.23) == []
        assert dates(1231) == []
        assert dates([10,1,2]) == []
        assert dates('2010-04-01') == []
        assert dates(['2010-04-01']) == []
        assert dates({'A':'none','B':'blah','C':'foo','D':'bar',"April's fools day":'2010-04-01'}) == ["April's fools day"]
        assert dates({0:'2003-10-09T18:18:18',1:'blah',2:'foo',3:'2007-11-14',4:'2010-04-01'}) == [0,3,4]


    def test_swap_dates( self ):
        assert swap_dates({'L':'2010-04-21','E':'2007-11-14'}) == (True,{'L':'2007-11-14','E':'2010-04-21'})
        assert swap_dates({'L':'2010-04-21','E':'foo'}) == (False,{'L':'2010-04-21','E':'foo'})
        assert swap_dates({'L':'foobar bla','E':'2007-11-14','D':'2003-10-09'}) == (True,{'L':'foobar bla','E':'2003-10-09','D':'2007-11-14'})
        (b,x) = swap_dates({'L':'2010-04-21','E':'2007-11-14','D':'2003-10-09'})
        assert b is True
        assert x == {'L':'2010-04-21','E':'2003-10-09','D':'2007-11-14'} or x == {'L':'2007-11-14','E':'2010-04-21','D':'2003-10-09'} or x == {'L':'2003-10-09','E':'2007-11-14','D':'2010-04-21'}
