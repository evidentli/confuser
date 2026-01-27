from unittest import TestCase
from confuser.confuser_schema import *
from confuser.confuser_params import params

class test_schema_map( TestCase ):
    def test_schema_map( self ):
        a = schema_map()
        assert a.name2obs == {}
        assert a.obs2name == {}

    def test_obscure_name( self ):
        a = schema_map()
        assert a.obscure_name(None) == None
        x = a.obscure_name("a")
        assert x != "a"
        assert len(x) == 12

        c = a.obscure_name("a.csv")
        assert c.endswith(".csv")

        y = a.obscure_name(x)
        assert y != x
        assert len(y) == 12
        d = {'a':1,'b':2,'c':3}
        e = a.obscure_name(d)
        assert len(e.keys()) == 3
        assert e[list(e.keys())[0]] == 1 or e[list(e.keys())[1]] == 1 or e[list(e.keys())[2]] == 1
        assert e[list(e.keys())[0]] == 2 or e[list(e.keys())[1]] == 2 or e[list(e.keys())[2]] == 2
        assert e[list(e.keys())[0]] == 3 or e[list(e.keys())[1]] == 3 or e[list(e.keys())[2]] == 3

        params.obscure_schema = False
        w = a.obscure_name("d")
        assert w == "d"
        z = a.obscure_name("a")
        assert z == x
        
        f = OrderedDict({'a':1,'b':2,'c':3})
        g = a.obscure_name(f)
        assert len(g.keys()) == 3
        assert g[list(g.keys())[0]] == 1
        assert g[list(e.keys())[1]] == 2 
        assert g[list(e.keys())[2]] == 3


    def test_real_name( self ): 
        a = schema_map()
        assert a.obscure_name(None) == None
        x = a.obscure_name("a")
        assert a.real_name(x) == "a"
        y = a.obscure_name(x)
        assert a.real_name(y) == x
        
