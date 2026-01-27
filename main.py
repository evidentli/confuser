import traceback
import argparse
import random
import sys
import os
from confuser.confuser import confuse,path_to_files
from confuser.confuser_params import params,synthea,param_description

def check_in_path( path ):
    if (path.endswith('csv') or path.endswith('csv/')):
        return path
    if (os.path.isdir(path)):
        if (os.path.isdir(os.path.join(path, "csv"))):
            return os.path.join(path, "csv")
        elif (os.path.isdir(os.path.join(path, "..", "csv"))):
            return os.path.join(path, "..", "csv")
        else:
         print(f"{path} has no csv directory and is itself not one")

    else:
         print(f"{path} is not a directory")

    return None


def check_out_path( out_path ):
    out_path=out_path.strip()

    if (not os.path.isdir(out_path)):
        try:
            os.mkdir(out_path)
        except FileNotFoundError:
            print(f'path to Confuser output ({os.path.normpath(out_path)}) does not exist, is not a directory and could not be created.')
            exit(1)

    return os.path.normpath(out_path)

def set_param( name_value_pair ):
    name_value=name_value_pair.split('=')
    if (len(name_value) != 2):
        sys.stderr.write(f"WARNING: invalid parameter specification. Specifications should be in the format name=value, not '{name_value_pair}' - parameter ignored\n")
        return
    name = name_value[0].strip()
    value = name_value[1].strip()
    if (not name in dir(params)):
        sys.stderr.write(f'WARNING: invalid parameter name {name} ignored.\n')
        sys.stderr.write(f'TIP: use --list-parameter to see available parameters.\n')
        return
    setattr(params,name,float(value))


def list_params( ):
    longest = 0
    for p in dir(params):
        if (not p.startswith('_')):
            if (len(p) > longest):
                longest = len(p)

    for p in dir(params):
        if (not p.startswith('_')):
            p_ = p.ljust(longest+2, ' ')
            print(f"{p_}: {getattr(params,p)}")
            print(f"{' '*(longest+4)}{param_description[p]}")
            print("")

def multiply_probabilities( ):
    for p in dir(params):
        if (p.startswith('p_')):
            setattr(params,p,params.mult*getattr(params,p))

def list_files( in_path ):
    files = path_to_files(in_path)
    for f in files:
        print(f)


def confuser_cli( ):
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', '-s', help='Seed for the random number generator', metavar='S', type=int, default=314)
    parser.add_argument('--in_path', '-i', help="path to the Synthea CSV directory", metavar='path', default='../synthea/output')
    parser.add_argument('--out_path', '-o', help="path to the Synthea CSV directory", metavar='path', default='../synthea/confusered')
    parser.add_argument('--verbose', '-v', help="explain what confuser is doing", default=False, action='store_true')
    parser.add_argument('--param', '-p', help="modify parameter", metavar='param=value', action='append')
    parser.add_argument('--list-parameters', '-l', help="list the available parameters and exit", action='store_true')
    parser.add_argument('--list-files', '-f', help="list the files that will be proccssed and exit", action='store_true')
    parser.add_argument('--mult', '-m', help='a number between 0 and 1 (inclusive) that will multiply all probability parameter (i.e. those that start with p_)', metavar='M', type=float, default=1.0)

    args = parser.parse_args()
    params.mult = args.mult

    multiply_probabilities()

    in_path = check_in_path(args.in_path)

    if (args.list_files):
        list_files(in_path)
        exit(0)

    if (args.param != None):
        for p in args.param:
            set_param(p)

    random.seed(int(args.seed))

    out_path = check_out_path(args.out_path)

    if (args.list_parameters):
        list_params()
        exit(0)

    try:
        confuse(seed=args.seed, in_path=in_path, out_path=out_path, verbose=args.verbose)
    except Exception as e:
        print('------------------------')
        print(f'Exception: {e}')
        print(traceback.format_exc())
        print('------------------------')


if __name__ == '__main__':
    confuser_cli()
