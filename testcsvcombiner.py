import unittest
import os
import csvcombiner
import csv
import sys
from io import StringIO


class MyTestCase(unittest.TestCase):
    temp = "test.csv"
    args = ["csvcombiner.py", "fixtures/accessories.csv", "fixtures/clothing.csv", "fixtures/household_cleaners.csv"]
    failcase = [" ", "household.csv", "fixture/clothing.excel",
                "test/accessories_no_value.csv", "test/accessories_diff_header.csv"]

    def setUp(self):
        self.output = StringIO()
        sys.stdout = self.output
        self.test_output = open(self.temp, 'w+')

    def tearDown(self):
        if os.path.exists(self.temp):
            os.remove(self.temp)
        self.test_output.close()

    def test_validate_file(self):
        for case in self.failcase:
            self.assertEqual(csvcombiner.validate_file(case), False)

    def test_csv_combiner(self):
        csvcombiner.combine_file(self.args)
        self.test_output.write(self.output.getvalue())

        #check if all the of row is added.
        with open(self.temp) as ftest:
            testfile = csv.reader(ftest)
            header = next(testfile)
            for arg in self.args[1:]:
                with open(arg) as f:
                    # check header
                    file = csv.reader(f)
                    file_header = next(file)
                    self.assertEqual(header[0:2], file_header[0:2])
                    # check row values
                    for line, testline in zip(file, testfile):
                        self.assertEqual(line[0:2], testline[0:2])
                        self.assertEqual(os.path.basename(arg), testline[2])


if __name__ == '__main__':
    unittest.main()
