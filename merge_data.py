#!/usr/bin/env python3

import csv
import os
UPDATE_DIR = 'update-files/'
OUTPUT_FILE = 'result.csv'


class Record:

    def __init__(self, data):
        self.attributes = dict()
        for attribute, value in data:
            self.attributes[attribute] = value

    def __str__(self):
        for key, value in self.attributes.items():
            print("{}: {}".format(key, value))
        return ''


class Database:

    def __init__(self, in_file):
        self.filename = in_file
        self.records = list()
        self.headers = list()
        self.raw_data = list()

        with open(self.filename, mode='r', encoding='utf-8') as master_db:
            reader = csv.reader(master_db)
            self.raw_data = self.listed_data(reader)

        self.headers = self.raw_data[0]
        for row in self.raw_data[1:]:
            entry = Record(zip(self.headers, row))
            self.records.append(entry)

    def __str__(self):
        for record in self.records:
            print(record)
        return ''

    def listed_data(self, reader):
        """
        Return a list of lists corresponding to data from a csv.reader object.
        """
        result = []
        for line in reader:
            result.append(line)
        return result

    def update(self, record):
        pass

    def merge(self, db2):
        delta_db = Database(db2)
        pass

    def export(self, out_filename='result.csv'):
        query = input("Enter output filename: ")
        if query == '':
            query = out_filename
        with open(query, encoding='utf-8', mode='w') as out_file:
            writer = csv.DictWriter(out_file, fieldnames=self.headers)
            writer.writeheader()
            for record in self.records:
                writer.writerow(record.attributes)

    def print_data(self):
        for record in self.records:
            print(record)


def filepicker():
    d = {}
    files = os.listdir(os.curdir)
    files = [f for f in files if os.path.isfile(f)]
    for index, filename in enumerate(files, 1):
        d[index] = filename
        print("({}): {}".format(index, filename))
    choice = int(input("Enter the number of the file to open: "))

    return d[choice]


if __name__ == "__main__":
    # db = input("Enter the name of the file to update: ").strip()
    db = filepicker()
    if db[-4:] != '.csv':
        print("Error: File must end in \".csv\"")
    else:
        print('Opening "{}"...'.format(db))
        database = Database(db)
        database.print_data()
        database.export()