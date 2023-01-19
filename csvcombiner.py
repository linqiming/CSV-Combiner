import os.path as path
import sys
import pandas as pd
import csv


def validate_file(args):
    """ensure correct csv file are inputted by user"""

    if len(args) <= 1:
        print("Error: No input file")
        return False

    preheader = None
    for arg in args[1:]:
        if not arg.endswith('.csv'):
            print(f"Error: File {arg} is not in csv file")
            return False
        if not path.exists(arg):
            print(f"Error: File {arg} does not exist")
            return False

        with open(arg) as f:
            file = csv.reader(f)
            file_header = next(file)
            if preheader is None:
                preheader = file_header
            else:
                if file_header != preheader:
                    print("Error: Files does not have same columns")
                    return False
            if len(list(file)) == 0:
                print(f"Error: File {arg} does not contain data")
                return False
    return True


def combine_file(args):
    """combine all the files"""

    header = True
    chunksize = 10000

    if validate_file(args):
        for file in args[1:]:
            for data in pd.read_csv(file, chunksize=chunksize, escapechar='\\'):
                data['filename'] = path.basename(file)
                print(data.to_csv(header=header, index=False, chunksize=chunksize, doublequote=False,
                                  lineterminator='\n', quoting=csv.QUOTE_ALL, escapechar='\\'), end='')
                header = False  # exclude header after the first csv file
    else:
        return


def main():
    combine_file(sys.argv)


if __name__ == '__main__':
    main()
