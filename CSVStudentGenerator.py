import csv #imports csv module
from knackpy import Knack


filters = {
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
    include_ids =False,
    filters = filters
)

x = kn.data
#paste AWS code and modify date 
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
master_bucket_name='itexpertcertificate20205'
master_bucket_status=check_bucket(master_bucket_name)
print ("bucket_status ="+ str(master_bucket_status))
if master_bucket_status == False:
            create_bucket(master_bucket_name)


def check_folder(foldername):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('itexpertcertificate20205')
    objs = list(bucket.objects.filter(Prefix=foldername))
    if(len(objs)>0):
        return True
    else:
        return False


def check_file(filename):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('itexpertcertificate20205')
    objs = list(bucket.objects.filter(Prefix=filename))
    if(len(objs)>0):
        return True
    else:
        return False


#define path where is student data has been saved.
studentdata = r"C:\Maggie\Internship\\test.csv"
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
        date = date.strip(' \t\n\r')
        #date = date.replace(date[:11]," ")
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
        imagefile = fullName + "_"+ cert_name + ".pdf"
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
            s3.Object(master_bucket_name , key).put(Body=imagebuffer)
            #write_file(bucket_name, master_bucket_name, key)
        else:
            print ("Key:" + key +" File exists!")
       
        #file_url = 'https://'+master_bucket_name+'.s3.us-east-2.amazonaws.com/'+key
        fileurl = f"https://{master_bucket_name}.s3.{region}.amazonaws.com/{key}"
        print(fileurl)
        print (key)  
