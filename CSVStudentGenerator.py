import csv #imports csv module

with open ('test.csv', 'w', newline='') as fp: #opens a blank csv file
    a = csv.writer(fp,delimiter = ",")
    l = [('Test', 'Result_2', 'Result_3', 'Result_4'), (1, 2, 3, 4), (5, 6, 7, 8)] #data to be inserted into csv file
    m = zip(*l) #Pairs each string with an integer
    a.writerows(m) #calls writerows function to categorize data in csv file
