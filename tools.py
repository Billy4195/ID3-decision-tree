import csv

def read_csv_file(filename):
    data = []
    with open(filename) as csvfile:
        content = csv.reader(csvfile,delimiter=',')
        for row in content:
            if len(row) > 0:
                row[0] = float(row[0])
                row[1] = float(row[1])
                row[2] = float(row[2])
                row[3] = float(row[3])
                data.append(tuple(row))

    return data
