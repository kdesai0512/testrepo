import csv #imports csv module
from knackpy import Knack


<<<<<<< HEAD
filters = { #Applies filters in the csv file to only list students that have completed the class
=======
filters = {
>>>>>>> 3c2b533cba02018d733f6a3f8e3653cd18e63e7d
      'match': 'and',
      'rules': [
        {
          'field':'field_148',
          'operator':'is',
          'value':'Complete'
        },
        {
          'field':'field_209',
          'operator':'is',
          'value':''
        }
      ]
    }




kn = Knack (
    obj = 'object_17', #This is found on the website url for the certification object
    app_id = '5ee26710da32c300153905ca',
    api_key = 'abde5d40-ae8d-11ea-8cd1-1dc626a4204b',
<<<<<<< HEAD
    include_ids =False, 
=======
    include_ids =False,
>>>>>>> 3c2b533cba02018d733f6a3f8e3653cd18e63e7d
    filters = filters
)

x = kn.data
#paste AWS code and modify date 
<<<<<<< HEAD
kn.to_csv("cert.csv")




#This program has been created to read CSV file (columns: id, fullName, course name, date) and create a txt/pdf file per student specific record in respective AWS S3 bucket 

aws_access_key_id = ""
aws_secret_access_key = ""
region="us-east-2"


=======
kn.to_csv("test.csv")

aws_access_key_id = ""
#"AKIAJVYSWZSO4E6DF6GQ"
aws_secret_access_key = ""
#"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"
region="us-east-2"



#This program has been created to read CSV file (columns: id, fullName, course name, date) and create a txt/pdf file per student specific record in respective AWS S3 bucket 

aws_access_key_id = ""
aws_secret_access_key = ""
region="us-east-2"


>>>>>>> 3c2b533cba02018d733f6a3f8e3653cd18e63e7d
import logging
import boto3
import botocore
from botocore.exceptions import ClientError
from boto3.s3.transfer import S3Transfer
from PIL import Image, ImageDraw, ImageFont
import io

import os

# define path where  genreated pdf files will be saved
pdfFolder = 'C:\Maggie\Internship'

if not os.path.exists(pdfFolder):
    os.makedirs(pdfFolder)


# List out ALL existing buckets

def listbucket():
    s3= boto3.client('s3')
    response=s3.list_buckets()
    print(response) # print list of bucket in JSON format

    # output the bucket names
    buckets= [bucket['Name'] for bucket in response['Buckets']]
    print("Buckets Name: %s" % buckets)



# create a new bucket
def create_bucket (bucket_name):
    
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    
    
# check bucket exist
def check_bucket(bucket_name):
    s3=boto3.resource('s3')
    bucket =s3.Bucket(bucket_name)
    if bucket.creation_date:
        print("the bucket exists")
        return True
    else:
        print("the bucket does not exist")
        return False
 

def write_file(bucket_name, master_bucket_name, key):
    credentials = {'aws_access_key_id': aws_access_key_id,'aws_secret_access_key': aws_secret_access_key}
    client = boto3.client('s3', 'us-east-2', **credentials)
    transfer = S3Transfer(client)
    transfer.upload_file(bucket_name, master_bucket_name, key, extra_args={'ACL': 'public-read'})
    file_url = '%s/%s/%s' % (client.meta.endpoint_url, bucket, key)


    
#create master bucket
<<<<<<< HEAD
master_bucket_name='itexpertcertificate2085'
=======
master_bucket_name='itexpertcertificate20205'
>>>>>>> 3c2b533cba02018d733f6a3f8e3653cd18e63e7d
master_bucket_status=check_bucket(master_bucket_name)
print ("bucket_status ="+ str(master_bucket_status))
if master_bucket_status == False:
            create_bucket(master_bucket_name)


def check_folder(foldername):
    s3 = boto3.resource('s3')
<<<<<<< HEAD
    bucket = s3.Bucket('itexpertcertificate2085')
=======
    bucket = s3.Bucket('itexpertcertificate20205')
>>>>>>> 3c2b533cba02018d733f6a3f8e3653cd18e63e7d
    objs = list(bucket.objects.filter(Prefix=foldername))
    if(len(objs)>0):
        return True
    else:
        return False


def check_file(filename):
    s3 = boto3.resource('s3')
<<<<<<< HEAD
    bucket = s3.Bucket('itexpertcertificate2085')
=======
    bucket = s3.Bucket('itexpertcertificate20205')
>>>>>>> 3c2b533cba02018d733f6a3f8e3653cd18e63e7d
    objs = list(bucket.objects.filter(Prefix=filename))
    if(len(objs)>0):
        return True
    else:
        return False


#define path where is student data has been saved.
<<<<<<< HEAD
studentdata = "/Users/udaymalik/Documents/ITEXPS/cert.csv"
=======
studentdata = r"C:\Maggie\Internship\\test.csv"
>>>>>>> 3c2b533cba02018d733f6a3f8e3653cd18e63e7d
viewfile = open(studentdata, "r")
data=viewfile.readlines()
recordcount=len(data)

for line in data:
    if(recordcount>0):
        id = (line.split(",")[5]) #student 
        fullName=(line.split(",")[6]) # first name

        fullName= fullName.strip(' \t\n\r')

        cert_name=(line.split(",")[3]) # course name
        cert_name= cert_name.strip(' \t\n\r')
        date = (line.split(",")[2]) # date
        date = date[:10]
        date = date.strip(' \t\n\r')
<<<<<<< HEAD
=======
        #date = date.replace(date[:11]," ")
>>>>>>> 3c2b533cba02018d733f6a3f8e3653cd18e63e7d
        foldername = fullName+str(id)
        print ("sub_bucket_name=",foldername)
        #define keystatus
        sub_bucket_status = check_folder(foldername)
        sub_folder_name = foldername
        # calling...create a bucket/call function
        if sub_bucket_status == False:
            s3 = boto3.client('s3')
            s3.put_object(Bucket = master_bucket_name, Key =(sub_folder_name))
        else:
            print ("Sub_bucket:" + foldername +" sub folder exists!")
            
        #create a stream
        imagebuffer = io.BytesIO()
        im = Image.open("C:\Maggie\Internship\\finalCertificate.jpg")
        d = ImageDraw.Draw(im)
        W = 844
        text_color = (0, 0, 0)
        font = ImageFont.truetype("constani.ttf", 36)
        w, h = d.textsize(fullName, font)
        location = ((W-w)/2, 227)
        d.text(location, fullName, fill = text_color, font = font)
        w, h = d.textsize(cert_name, font)
        location = ((W-w)/2, 360)
        d.text(location, cert_name, fill = text_color, font = font)
        w, h = d.textsize(date, font)
        location = ((W-w)/2, 475)
        d.text(location,date, fill = text_color, font = font)
<<<<<<< HEAD
        imagefile = fullName +"_"+ id + "_"+ cert_name + ".pdf"
=======
        imagefile = fullName + "_"+ cert_name + ".pdf"
>>>>>>> 3c2b533cba02018d733f6a3f8e3653cd18e63e7d
        #get buffer
        im.save(imagebuffer,"PDF")
        imagebuffer.seek(0)# rewind pointer back to start
        s3 = boto3.resource('s3',region_name='us-east-2', aws_access_key_id='', aws_secret_access_key='')
        #define key
        key = foldername+'/'+imagefile
        # calling...checking key/call function
        filefolder_status = check_file(key)
        
        if filefolder_status == False:
            print ("Key :" + key +" File does not exist!")
            s3.Object(master_bucket_name , key).put(Body=imagebuffer, ACL = 'public-read')
            #write_file(bucket_name, master_bucket_name, key)
        else:
            print ("Key:" + key +" File exists!")
       
        #file_url = 'https://'+master_bucket_name+'.s3.us-east-2.amazonaws.com/'+key
        fileurl = f"https://{master_bucket_name}.s3.{region}.amazonaws.com/{key}"
        print(fileurl)
        print (key)  
<<<<<<< HEAD


#This program has been created to insert a certificate from S3 to our Knack application.

import logging
import boto3
import botocore
import io
import json
import os
import requests

def retrievebucket():
    s3_client = boto3.client('s3')
    bucket_location = s3_client.get_bucket_location(Bucket= 'itexpertcertificate2085')
    
    response = s3_client.list_objects(Bucket='itexpertcertificate2085')

    for object in response['Contents']:
        underscorenumber = 0
        for i in range(0, len(object['Key'])):
            if object['Key'][i] == "_":
                underscorenumber += 1
        if "pdf" in object['Key'] and underscorenumber == 2:
            officialstudentid = parsestudentid(object['Key'])
            officialcoursename = parsecoursename(object['Key'])
            url = "https://s3.%s.amazonaws.com/%s/%s" % (bucket_location['LocationConstraint'], 'itexpertcertificate2085', object['Key'])
            updateRecord(officialstudentid, officialcoursename, url)
    
def parsestudentid(keystr):
    newpdfstr = keystr[(keystr.index("_") + 1):]
    studentid = newpdfstr[0:newpdfstr.index("_")]
    return studentid


def parsecoursename(keystr):
    newpdfstr = keystr[(keystr.index("_") + 1):]
    studentid = newpdfstr[0:newpdfstr.index("_")]
    coursename = newpdfstr[(newpdfstr.index("_") + 1):newpdfstr.index(".")]
    return coursename
#------------------------------------------------------------------------------------------------------------------------------------------------

def getCertificationForStudentAndCourse(studentidfromcertification, courseName):
    print(f'searching for student : {studentidfromcertification} and course name : {courseName}')
    
    response = requests.get("https://api.knack.com/v1/objects/object_17/records",
        headers={
            "X-Knack-Application-Id":"5ee26710da32c300153905ca",
            "X-Knack-REST-API-Key":"abde5d40-ae8d-11ea-8cd1-1dc626a4204b",
            "Content-Type":"application/json"
        }
    )
    jsonresponse = response.json()
    #print(json.dumps(jsonresponse, indent = 4, sort_keys=True))
    table = jsonresponse["records"];
    for i in range(0, len(table)):        
        courseobject = table[i]["field_147_raw"]
        courseid = courseobject[0]["id"];
        courseidentifier = courseobject[0]["identifier"];
        #print(f' courseid : { courseid } courseidentifier : { courseidentifier}')

        studentobject = table[i]["field_146_raw"]
        studentid = studentobject[0]["id"];
        studentidentifier = studentobject[0]["identifier"];
        #print(f' studentid : { studentid } studentidentifier : { studentidentifier}')
        
        if (courseidentifier == courseName and studentidentifier ==  studentidfromcertification):
            print(f' certificate record id : {table[i]["id"]}')
            return table[i]["id"]

    return "";


def updateRecord(studentID, courseName, certificateurl):
    if studentID == "" or courseName == "":
        return
    
    recid = getCertificationForStudentAndCourse(studentID, courseName)

    if recid == "":
        return

    print(f'Updating student id :{studentID}, Course Name : {courseName}')

    url = "https://api.knack.com/v1/objects/object_17/records/" + recid

    print(f'url is {url}.')

    field_data = { 'field_209' : certificateurl }
    
    response = requests.put(url,
        headers={
            "X-Knack-Application-Id":"5ee26710da32c300153905ca",
            "X-Knack-REST-API-Key":"abde5d40-ae8d-11ea-8cd1-1dc626a4204b",
            "Content-Type":"application/json"
        },
        data=json.dumps(field_data)
    )
    print(response.text)
    

retrievebucket()



