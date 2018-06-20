#!/usr/bin/env python3

import csv
import os
UPDATE_DIR = 'update-files/'


class Record:

    def __init__(self, data):
        self.attributes = dict()
        for attribute, value in data:
            self.attributes[attribute] = value

    def __str__(self):
        for key, value in self.attributes.items():
            print("{}: {}".format(key, value))
        return ''

    def set_key(self, key):
        self.key = key


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
        common_headers = [x for x in self.headers if x in delta_db.headers]
        self.headers.extend(
            [x for x in delta_db.headers if x not in self.headers])
        key = self.headerpicker(common_headers)
        records_temp = self.records[:]
        for each in delta_db.records:
            record = self.fetch_record(key, each, records_temp)
            if record:
                record.attributes.update(each.attributes)
        self.records = records_temp

    def export(self, out_filename='RESULT.csv'):
        query = input("Enter output filename: ")
        if query == '':
            query = out_filename
        with open(query, encoding='utf-8', mode='w') as out_file:
            writer = csv.DictWriter(out_file, fieldnames=self.headers)
            writer.writeheader()
            for record in self.records:
                writer.writerow(record.attributes)

    def fetch_record(self, key, record2, records_temp):
        for record in self.records:
            if record.attributes[key] == record2.attributes[key]:
                return record
        records_temp.append(record2)

    def print_data(self):
        for record in self.records:
            print(record)

    def headerpicker(self, common_headers):
        d = {}
        for index, header in enumerate(common_headers, 1):
            d[index] = header
            print("[{}] {}".format(index, header))
        choice = int(
            input("Enter the number of the header to use as key: ").strip())
        return d[choice]


def filepicker(dir=os.curdir):
    d = {}
    files = os.listdir(dir)
    files = [f for f in files if os.path.isfile(f) and '.csv' in f[-4:]]
    for index, filename in enumerate(files, 1):
        d[index] = filename
        print("[{}] {}".format(index, filename))
    choice = int(input("\n>").strip())
    print("-" * 20, "\n")
    if dir == os.curdir:
        return d[choice]
    else:
        return dir + d[choice]


def folderpicker():
    d = {}
    dirs = os.listdir(os.curdir)
    dirs = [x for x in dirs if os.path.isdir(x)]
    for index, dirname in enumerate(dirs, 1):
        d[index] = dirname
        print("[{}] {}".format(index, dirname))
    choice = int(input("\n>").strip())
    print("-" * 20, "\n")

    return d[choice]


if __name__ == "__main__":
    # db = input("Enter the name of the file to update: ").strip()
    print("Pick a file to open:")
    db = filepicker()
    print("Pick an update folder:")
    update_folder = folderpicker()
    database = Database(db)
    query = ''
    while query.upper() != 'N':
        query = 'N'
        print("Pick a file to merge:")
        try:
            database.merge(filepicker(update_folder + '/'))
            print("Merge successful!")
        except TypeError:
            print("Merge unsuccessful.")
        query = input("Merge another database? y/N\n>")
    database.export()
