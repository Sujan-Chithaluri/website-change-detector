import mysql.connector
import datetime
import pandas
import time
import os
import uuid
import cv2
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from skimage.metrics import structural_similarity
from PIL import Image

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders 

from datetime import datetime

from imagetotext import ocr_core

debug=True
frequency=False

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("websitemonitoring2357@gmail.com", "Websitemonitoring@2357")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="sujan@mysql@35",
  database="majorproject"
)

now = datetime.now()

if frequency:
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM tasks where nextcheck=NULL or nextcheck<%s",(now,))
    myresult = mycursor.fetchall()
else:
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM tasks ")
    myresult = mycursor.fetchall()

options = webdriver.ChromeOptions()
options.headless = True

if(debug):
    print("fetching pages.....")
    
for task in myresult:
    # print(task)
    
    id= task[11]
    name=id+'-new.png'
    path=os.path.join('static', 'original-new','')
    path=path+name
    
    driver = webdriver.Chrome(options=options)
    driver.get(task[1])
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(1100, required_height+10)

    driver.find_element_by_tag_name('body').screenshot(path)
    driver.quit()

if(debug):
    print("Cropping selected portion.....")    
    
for task in myresult:
    
    id= task[11]
    name=id+"-new.png"
    path=os.path.join('static', 'original-new','')
    path=path+name
    
    original=Image.open(path)
    width,height=original.size
    top=task[7]
    left=task[8]
    right=task[8]+task[9]
    bottom=task[7]+task[10]
    
    name=name.replace("-new.png","-new-cropped.png")
    path=os.path.join('static', 'cropped-new','')
    path=path+name
    
    cropped=original.crop((left,top,right,bottom))
    cropped.save(path)

if(debug):
    print("Comparing with previous images.....")    
     
for task in myresult:
    #print(task)
    id= task[11]
    
    name1=id+"-old-cropped.png"
    name2=id+"-new-cropped.png"
    name3=id+"-compare.png"
    
    path1=os.path.join('static', 'cropped-old','')
    path2=os.path.join('static', 'cropped-new','')
    path3=os.path.join('static', 'compare','')
    
    
    before = cv2.imread(path1+name1)
    after = cv2.imread(path2+name2)
    k=cv2.imread(path2+name2)
    
    # Image.open(path1+name1).show()
    # Image.open(path2+name2).show()
    
    before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
    
    (score, diff) = structural_similarity(before_gray, after_gray, full=True)
    
    score=score*100
    dissimilarity=100-score
    
    if(task[4]=='TINY'):
        usersens=0.00001
    elif(task[4]=='LOW'):
        usersens=25
    elif(task[4]=='MEDIUM'):
        usersens=50 
    elif(task[4]=='HIGH'):
        usersens=75 
        
    # print(task[4])
    # print("Image similarity", score)
    # print("Image Dissimilarity", dissimilarity)
    
    proceed = True
    kp=[]
    if len(task[5]) > 0:
        keywords=task[5].split(',')
        extractedtext=ocr_core(path2+name2)
        cleantext=" ".join(extractedtext.split())
    
        for word in keywords:
            if word in cleantext:
                kp.append(word)
        
        # print("Keywords : ",task[5])
        # print(keywords)
        # print("Text in the image is : ",extractedtext)
        # print("Clean Text in the image is : ",cleantext)
        # print("Keywords and Phrases found are :",kp)
        
        if len(kp)==0:
            proceed= False
    
    if(dissimilarity >= usersens and proceed ):
    
        diff = (diff * 255).astype("uint8")
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        mask = np.zeros(before.shape, dtype='uint8')
        filled_after = after.copy() 
        
        for c in contours:
            area = cv2.contourArea(c)
            if area > 40:
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)
                cv2.drawContours(mask, [c], 0, (255,255,255), -1)
                
        red_mask = np.copy(k)
        red_mask[(mask==255).all(-1)] = [0,0,255]
        red_mask= cv2.addWeighted(red_mask,0.4,k,0.6, 0,red_mask)
        cv2.imwrite(path3+name3,red_mask)   
        
        msg=MIMEMultipart()
        msg['From']="websitemonitoring2357@gmail.com"
        msg['To']=task[6]
        
        msg['Subject'] = "Detected change in :"+task[2].upper()
        body = "Check the website : \t"+task[1]
        
        if len(kp)>0:
            body=body+"\nKeywords and Phrases set by you : \t"+str(keywords).strip('[]')
            body=body+"\nKeywords and Phrases detected   : \t"+str(kp).strip('[]')
         
        #print(body)
        
        msg.attach(MIMEText(body, 'plain'))
        
        file1="Before.png"
        file2="After.png"
        file3="Compare.png"
        
        a1 = open(path1+name1,"rb")
        a2 = open(path2+name2,"rb")
        a3 = open(path3+name3,"rb")
        
        p=MIMEBase('application', 'octet-stream')
        p.set_payload((a1).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % file1)
        msg.attach(p)
        
        p=MIMEBase('application', 'octet-stream')
        p.set_payload((a2).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % file2)
        msg.attach(p)
        
        p=MIMEBase('application', 'octet-stream')
        p.set_payload((a3).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % file3)
        msg.attach(p)
        
        text = msg.as_string()
        s.sendmail("websitemonitoring2357@gmail.com",task[6],text)
       
if(debug):
    print("Replacing old with new images.....")    
 
for task in myresult:
    id= task[11]
    
    name1=id+"-old-cropped.png"
    name2=id+"-new-cropped.png"
    
    name3=id+"-old.png"
    name4=id+"-new.png"
       
    path1=os.path.join('static', 'cropped-old','')
    path2=os.path.join('static', 'cropped-new','')
    
    path3=os.path.join('static', 'original-old','')
    path4=os.path.join('static', 'original-new','')
    
    temp1 = cv2.imread(path2+name2)
    temp2 = cv2.imread(path4+name4)
    
    cv2.imwrite(path1+name1,temp1)
    cv2.imwrite(path3+name3,temp2)
    
s.quit()  

if(debug):
    print("Setting the value for next check.....") 

for x in myresult:
    if x[3]=="15 mins":
        temp=pandas.Series(now).dt.ceil('15min')[0]
       
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        mydb.commit()
    
    if x[3]=="30 mins":
        temp=pandas.Series(now).dt.ceil('30min')[0]
        
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        mydb.commit()
   
    if x[3]=="1 hour":
        temp=pandas.Series(now).dt.ceil('1H')[0]
        
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        mydb.commit()
   
    if x[3]=="3 hours":
        temp=pandas.Series(now).dt.ceil('3H')[0]
        
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        mydb.commit()

    if x[3]=="6 hours":
        temp=pandas.Series(now).dt.ceil('6H')[0]
        
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        mydb.commit()


    if x[3]=="1 day":
        temp=pandas.Series(now).dt.ceil('1D')[0]
        temp=temp+pandas.DateOffset(hours=9)
        
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        mydb.commit()
        

    if x[3]=="1 week":
        temp=pandas.Series(now).dt.ceil('7D')[0]
        temp=temp+pandas.DateOffset(hours=9)
      
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        mydb.commit()        