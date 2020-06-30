import csv #imports csv module
from knackpy import Knack

#with open ('test.csv', 'w', newline='') as fp: #opens a blank csv file
 #   a = csv.writer(fp,delimiter = ",")
  #  l = [('Test', 'Result_2', 'Result_3', 'Result_4'), (1, 2, 3, 4), (5, 6, 7, 8)] #data to be inserted into csv file
   # m = zip(*l) #Pairs each string with an integer
    # a.writerows(m) #calls writerows function to categorize data in csv file
kn = Knack (
    obj = 'object_17', #This is found on the website url for the certification object
    app_id = '5ee26710da32c300153905ca',
    api_key = 'abde5d40-ae8d-11ea-8cd1-1dc626a4204b'
)

x = kn.data
print(x)

kn.to_csv('test.csv')