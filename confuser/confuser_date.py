from dateutil import parser
import random

def is_date( string ):
    if (not isinstance(string, str) or len(string) < 6):
        return False

    try:
        parser.parse(string).isoformat()
    except:
        return False

    return True

def dates( values ):
    date_keys = []
    if isinstance(values, dict):
        for key in values.keys():
            if is_date(values[key]):
                date_keys.append(key)

    return date_keys

def swap_dates( values ):
    indeces = dates(values)

    if (len(indeces) < 2):
        return False,values

    d1 = random.choice(indeces)
    indeces.remove(d1)
    d2 = random.choice(indeces)

    tmp = values[d1]
    values[d1] = values[d2]
    values[d2] = tmp

    return True,values


    

