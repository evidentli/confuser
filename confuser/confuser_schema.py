from collections import OrderedDict
from .confuser_str import get_obscure_str
from .confuser_params import params
import types

class schema_map:
    def __init__( self ):
        self.name2obs = {}
        self.obs2name = {}

    def obscure_name( self, name ):
        if (name == None):
            return None

        if (type(name) == type("")):
            if (name in self.name2obs.keys()):
                return self.name2obs[name]

            if (params.obscure_schema == True):
                obs = get_obscure_str(12)
                if (name.endswith(".csv")):
                    obs += ".csv"
            else:
                obs = name

            self.name2obs[name] = obs
            self.obs2name[obs] = name
            return obs

        obs = None
        if (type(name) == type({}) or type(name).__name__ == 'dict'):
            obs = {}

        if (type(name).__name__ == 'OrderedDict'):
            obs = OrderedDict()

        if (obs != None):
            for key in name.keys():
                o = self.obscure_name(key)
                obs[o] = name[key]

            return obs

        raise TypeError(f'unrecognized type: {type(name).__name__}')


    def real_name( self, obs ): 
        if (obs == None):
            return None

        try:
            return self.obs2name[obs]
        except KeyError:
            return None

resolver = schema_map()
