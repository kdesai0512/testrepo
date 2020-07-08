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
    bucket_location = s3_client.get_bucket_location(Bucket= 'itexpertcertificate2021')
    
    response = s3_client.list_objects(Bucket='itexpertcertificate2021')

    for object in response['Contents']:
        underscorenumber = 0
        for i in range(0, len(object['Key'])):
            if object['Key'][i] == "_":
                underscorenumber += 1
        if "pdf" in object['Key'] and underscorenumber == 2:
            officialstudentid = parsestudentid(object['Key'])
            officialcoursename = parsecoursename(object['Key'])
            url = "https://s3.%s.amazonaws.com/%s/%s" % (bucket_location['LocationConstraint'], 'itexpertcertificate2021', object['Key'])
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

