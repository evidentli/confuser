import csv
import random
import os
from .confuser_schema import resolver

class split_writer: 
    def __init__( self, fieldnames, out_path ):
        self.fieldnames = list(fieldnames)
        pk = self.fieldnames[0]
        others = self.fieldnames[1:]
        random.shuffle(others)
        self.fieldnames_1 = list() 
        self.fieldnames_1 += pk #append(pk)
        self.fieldnames_1 += others[int(len(others)/2.0):]
        self.fieldnames_2 = list()
        self.fieldnames_2.append(pk)
        self.fieldnames_2 += others[:int(len(others)/2.0)]

        if (out_path.endswith('.csv')):
            out_path = out_path[:-4]
        out_path_1 = os.path.join(os.path.dirname(out_path),'a_' + os.path.basename(out_path) + '.csv')
        out_path_2 = os.path.join(os.path.dirname(out_path),'b_' + os.path.basename(out_path) + '.csv')
        self.file_1 = open(out_path_1, 'w')
        self.file_2 = open(out_path_2, 'w')
        self.writer_1 = csv.DictWriter(self.file_1, fieldnames=self.fieldnames_1)
        self.writer_2 = csv.DictWriter(self.file_2, fieldnames=self.fieldnames_2)

    def writeheader( self ):
        self.writer_1.writeheader()
        self.writer_2.writeheader()

    def writerow( self, row ):
        row1 = {}
        row2 = {}
        for key in row.keys():
            if (key in self.writer_1.fieldnames):
                row1[key] = row[key]
            if (key in self.writer_2.fieldnames):
                row2[key] = row[key]
        self.writer_1.writerow(row1)
        self.file_1.flush()
        self.writer_2.writerow(row2)
        self.file_2.flush()

    def close( self ):
        self.file_1.close()
        self.file_2.close()

