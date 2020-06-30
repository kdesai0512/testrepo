import csv

with open ('test.csv', 'w', newline='') as fp:
    a = csv.writer(fp,delimiter = ",")
    l = [('Result_1', 'Result_2', 'Result_3', 'Result_4'), (1, 2, 3, 4), (5, 6, 7, 8)]
    m = zip(*l)
    a.writerows(m)
