#!/usr/bin/env python
#-*- coding:utf-8 -*


from optparse import OptionParser
import csv


def reorder(filename):

    if filename.endswith('.csv'):
        uid = filename[:-4]
        
    newfile = "ord_"+filename
    with open(filename, 'r') as infile, open(newfile, 'a') as outfile:
        # output dict needs a list for new column ordering
        fieldnames = ['rt', 'responses', 'trial_type', 'trial_index', 'time_elapsed', 'internal_node_id', 'stimulus', 'button_pressed', 'key_press', 'participant_id', 'offset', 'robot_rt', 'robot_error', 'response', 'correct', 'value']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            row['participant_id'] = uid
            # writes the reordered rows to the new file
            writer.writerow(row)
        
        
def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", help="file containing the raw experiment data", metavar="FILE")
    (options, args) = parser.parse_args()

    reorder(options.file)


if __name__ == '__main__':
    main()

