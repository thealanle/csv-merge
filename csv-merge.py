#!/usr/bin/env python3

import csv
import os


class Record:

    def __init__(self, data):
        """
        Store incoming {header:data} pairs in a dict
        """
        self.attributes = dict()
        for attribute, value in data:
            self.attributes[attribute.strip()] = value.strip()

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
        # self.in_data = list()

        with open(self.filename, mode='r', encoding='utf-8') as master_db:
            reader = csv.reader(master_db)
            self.in_data = self.listed_data(reader)

        self.headers = self.in_data[0]
        for row in self.in_data[1:]:
            entry = Record(zip(self.headers, row))
            self.records.append(entry)

        print("A database has been created from {}.\n".format(self.filename))

    def __str__(self):
        self.print_data()
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
        """
        Create a new database from a csv file, then compare its records with
        the master database. Update the records in the master database with data
        from the delta database.
        """
        delta_db = Database(db2)

        # Find common headers between the master and delta databases
        common_headers = [x for x in self.headers if x in delta_db.headers]

        # Any new headers found in the delta are added to the master
        self.headers.extend(
            [x for x in delta_db.headers if x not in self.headers])

        if len(common_headers) < 1:
            print("No shared headers were found. These files cannot be merged.")
        else:
            key = ''
            # Skip picker prompt if there is only one common header
            if len(common_headers) == 1:
                key = common_headers[0]
            else:
                key = self.headerpicker(common_headers)

            # Create a temp list for new records to be added to
            records_temp = list(self.records)

            # Iterate over new records and attempt to match to existing record
            for each in delta_db.records:
                record = self.fetch_record(key, each, records_temp)
                if record:
                    record.attributes.update(each.attributes)

            self.records = records_temp
            print("Merge successful!\n")

    def export(self, out_filename='RESULT.csv'):
        """
        Exports the database's records to a CSV.
        """

        query = input(
            "Enter output filename (Default = {}):\n>".format(out_filename))
        # Set filename to the default value if user doesn't enter one
        if query == '':
            query = out_filename

        with open(query, encoding='utf-8', mode='w', newline='\n') as out_file:
            writer = csv.DictWriter(out_file, fieldnames=self.headers)

            writer.writeheader()  # Write the headers to the first row
            for record in self.records:
                writer.writerow(record.attributes)

        print("Successfully output to {}".format(query))

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
        print("Enter the number of the header to use as key (Default = [1]).")
        for index, header in enumerate(common_headers, 1):
            d[index] = header
            print("[{}] {}".format(index, header))
        choice = input("\n>").strip()
        if choice == '':
            return d[1]
        return d[int(choice)]


def filepicker(dir=os.curdir):
    """
    Display a list of files in a directory and allow selection by the user.
    """
    choices = {}
    files = os.listdir(dir)
    files = sorted(
        [f for f in files if os.path.isfile(f) and '.csv' in f[-4:]])

    # Print the filenames with corresponding integers
    for index, filename in enumerate(files, 1):
        choices[index] = filename
        print("[{}] {}".format(index, filename))

    choice = int(input("\n>").strip())  # Prompt user for choice
    print("-" * 20, "\n")
    if dir == os.curdir:
        return choices[choice]
    else:
        return dir + choices[choice]


# def folderpicker():
#     d = {}
#     dirs = os.listdir(os.curdir)
#     dirs = [x for x in dirs if os.path.isdir(x)]
#     for index, dirname in enumerate(dirs, 1):
#         d[index] = dirname
#         print("[{}] {}".format(index, dirname))
#     choice = int(input("\n>").strip())
#     print("-" * 20, "\n")
#
#     return d[choice] + '/'


if __name__ == "__main__":
    # db = input("Enter the name of the file to update: ").strip()
    print("Pick a file to open:")
    db = filepicker()
    # print("Pick an update folder:")
    # update_folder = folderpicker()
    database = Database(db)
    query = ''
    while query.lower() != 'n':
        print("Pick a file to merge:")
        database.merge(filepicker())
        query = input("Merge another database? [y/N]\n>").strip()
        if query == '':
            query = 'N'
    database.export()
