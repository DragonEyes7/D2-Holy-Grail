import csv

class DataFeeder:
    def __init__(self, csv):
        csv = 'Data\\CSV\\UniqueList.csv'
        with open(csv, newline='') as csvFile:
            spamreader = csv.reader(csvFile, delimiter=',')