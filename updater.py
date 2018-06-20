#!/usr/bin/env python3

import csv
import os
UPDATE_DIR = 'update-files/'
OUTPUT_FILE = 'result.csv'


def merge_files(record, input_directory):
    """
    Given a master record, ingest files from the input directory and merge
    their data into the master record.
    """
    record_reader = csv.reader(record)
    record_rows = listed_data(record_reader)
    record_header = record_rows[0]
    record_ids = [x[0] for x in record_rows[1:]]

    for filename in os.listdir(input_directory):
        filepath = ''.join([input_directory, filename])
        print(filepath)

        with open(filepath, encoding='utf-8', mode='r') as input_data:

            data_reader = csv.reader(input_data)
            data_rows = listed_data(data_reader)
            data_header = data_rows[0]

            for col_index, header in enumerate(data_header):
                i = None
                try:
                    i = record_header.index(header)
                except ValueError:
                    record_header.append(header)
                    for record in record_rows[1:]:
                        record.append('')
                    i = record_header.index(header)
                print(i)
                print(record_header)
                for row in data_rows[1:]:
                    id = row[0].strip()
                    if id in record_ids:
                        print("ID: {} found!".format(id))
                        id_index = record_ids.index(id) + 1
                        record_rows[id_index][i] = row[col_index]
                    elif id not in record_ids:
                        print("ID: {} not found!".format(id))
                        new_record = [id]
                        for x in range(0, len(record_header) - 1):
                            new_record.append(list())
                        new_record[i] = row[col_index]
                        print(new_record, "has been added to the master record.")
                        record_rows.append(new_record)

    with open(OUTPUT_FILE, 'w') as output_file:
        output_writer = csv.writer(output_file)
        for row in record_rows:
            output_writer.writerow(row)


def listed_data(reader):
    """
    Return a list of lists corresponding to data from a csv.reader object.
    """
    result = []
    for line in reader:
        result.append(line)
    return result


if __name__ == '__main__':
    print(os.getcwd())
    record_file = input("Enter the name of the file to update: ")
    with open(record_file, mode='r+') as record:
        merge_files(record, UPDATE_DIR)
