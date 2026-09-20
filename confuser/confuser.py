import random
import sys
import csv
import os
import re
from .confuser_str import confuse_str
from .confuser_date import swap_dates
from .confuser_params import params,synthea
from .confuser_schema import resolver
from .confuser_split_writer import split_writer

class csv_writer:
    def __init__( self, out_file, fieldnames ):
        self.file = open(out_file, 'w', newline='')
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        self.fieldnames = self.writer.fieldnames

    def writeheader( self ):
        self.writer.writeheader()

    def writerow( self, row ):
        self.writer.writerow(row)

    def close( self ):
        self.file.close()

def get_new_writer( out_path, csv_file, row ):
    if (csv_file.endswith('.csv')):
            csv_file = csv_file[:-4]
    csv_file = os.path.basename(csv_file)
    obscured_file = resolver.obscure_name(csv_file + ".csv")
    obscured_headers = resolver.obscure_name(dict(row)).keys()
    writer = None
    r = random.random()
    if (r > 1 - params.p_split_table):
        writer = split_writer(out_path=os.path.join(out_path, obscured_file), fieldnames=obscured_headers)
    else:
        writer = csv_writer(os.path.join(out_path, obscured_file), obscured_headers)

    writer.writeheader()

    return writer


def switch_table( out_path, csv_file, row, writerCount ):
    if (csv_file.endswith('.csv')):
        csv_file = csv_file[:len(csv_file)-4] + '_' + str(writerCount) + '.csv'
    else:
        csv_file = csv_file + '_' + str(writerCount) + '.csv'

    return get_new_writer(out_path, csv_file, row)


def mutate_descriptions( row ):
    new_row = {}
    for col in resolver.obscure_name(row).keys():
        real_col = resolver.real_name(col)
        normalized_col = re.sub(r'\d+$', '', real_col.strip(' \"').upper()) if real_col != None else None
        if (normalized_col != None and normalized_col.endswith(synthea.desc_header)):
            new_row[col] = confuse_str(line=row[real_col])
        else:
            new_row[col] = row[real_col]

    return new_row


def misplace_row( row, writers ):
    if (len(writers) == 1):
        return "the ether"
    new_row = {}
    #pick a table
    r = random.randrange(len(writers))
    alternative_writer = writers[list(writers.keys())[r]]
    for col in row:
        if (resolver.obscure_name(col) in alternative_writer.fieldnames):
            new_row[col] = row[col]

    alternative_writer.writerow(resolver.obscure_name(new_row))
    return list(writers.keys())[r]


def drop_row( row ):
    return None

def drop_value( row ):
    new_row = row
    if (len(new_row) != 0):
        r = random.randrange(len(row))
        new_row[list(row)[r]] = 'NULL'

    return new_row
    

def dup_row( row ):
    if (row == None):
        return False
    return True


def path_to_files( in_path ):
    ret = []
    if (os.path.isdir(in_path)):
        for root, dirs, files in os.walk(in_path):
            for name in files:
                ret.append(os.path.join(root, name))
    else:
        ret.append(in_path)

    return ret


def confuse( seed, in_path, out_path, verbose ):
    random.seed(seed)
    print(f"confusing from {in_path} to {out_path}")

    writers = {}
    all_writers = []
    for in_file in path_to_files(in_path):
        if (os.access(in_file, os.R_OK)): 
            with open(in_file, 'r', newline='') as reader:
                # Use the CSV parser for headers so quoted and unquoted CSVs behave the same.
                row = dict.fromkeys(next(csv.reader(reader)), '')
            writers[in_file] = get_new_writer(out_path, in_file, row)
            all_writers.append(writers[in_file])
        else:
            print(f"could not find {in_file} in {in_path}") 

    reader = None
    writer = None

    try:
        for in_file in writers.keys():
            if (verbose):
                print(f'= processing {in_file}')
            with open(in_file, 'r', newline='') as in_f:
                reader = csv.DictReader(in_f)
                can_swap_dates = True
                duplicate = False
                writer = writers[in_file]
                current_writer_count = 0

                for row in reader:
                    row_written = False
                    row_obscured = False
                    new_row = row

                    if (random.random() > 1 - params.p_switch_table): 
                        writer = switch_table(out_path, os.path.basename(in_file), writerCount=current_writer_count, row=row)
                        all_writers.append(writer)
                        current_writer_count += 1
                        if (verbose):
                            new_file = in_file.replace(".csv", "_" + str(current_writer_count) + ".csv")
                            print(f'== switching to {new_file}') 
                    if (random.random() > 1 - params.p_omit_row):
                        if (verbose):
                            print(f'== dropping a row')
                        new_row = drop_row(new_row)
                    if new_row is not None:
                        if (random.random() > 1 - params.p_typo):
                            if (verbose):
                                print(f'== introducing typos')
                            new_row = mutate_descriptions(new_row)
                            row_obscured = True 
                        if (random.random() > 1 - params.p_swap_dates):
                            can_swap_dates,new_row = swap_dates(new_row)
                            if (verbose and can_swap_dates):
                                print(f'== swapping dates')
                        if (random.random() > 1 - params.p_drop_value):
                            if (verbose):
                                print(f'== dropping a value')
                            new_row = drop_value(new_row)
                        if (random.random() > 1 - params.p_misplace_row):
                            new_table = misplace_row(new_row, writers)
                            if (verbose):
                                print(f'== misplacing a row to {new_table}')
                            row_written = True
                            row_obscured = True           
                        if (random.random() > 1 - params.p_dup_row and row_written == False):
                            duplicate = dup_row(new_row) 
                            if (verbose and duplicate):
                                print(f'== duplicating a row')
                
                        if row_obscured == False:
                            new_row = resolver.obscure_name(new_row)

                        if row_written == False:
                            try:
                                #print(new_row)
                                writer.writerow(new_row)
                                if duplicate:
                                    writer.writerow(new_row)
                            except ValueError:
                                print(f"Can't write {new_row} to {type(writer.fieldnames)}:{writer.fieldnames} -- skipping")
                                print(resolver.name2obs)
                                #raise Exception(resolver.obscure_name(new_row).keys(), " mismatched ", writer.fieldnames)
            if (verbose):
                print(f'= mappings used:')
                print(resolver.obs2name)
                print(f'= reversed mapping used:')
                print(resolver.name2obs)
    finally:
        for writer in all_writers:
            writer.close()
