import time
import re
import os
import uuid

from PIL import Image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def takess(url):

    id= str(uuid.uuid4())
    name=id+'-old.png'
    path=os.path.join('static', 'original-old','')
    path=path+name
 
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    #name=url
    #name=name.lower()
    #name=name.replace("https://www.","")
    #name=re.sub("[^a-zA-Z\s]+"," ",name)
    #name=re.sub("(\s+)", "-",name)
    #name=name+'old.png'
    
    # name=str(hashlib.sha256(url.encode('utf-8')).hexdigest())
    # name=name+"-old.png"
       
    #path = 'C:/Users/DELL/VII Sem/Major Project/static/original-old/'+text
    #path = '/static/original-old/'+text
        
    driver.get(url)

    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(1100, required_height+10)

    driver.find_element_by_tag_name('body').screenshot(path)

    driver.quit()
    
    return id
    
#print(takess("http://www.google.com/"))

def cropss(id,t,l,w,h):
    name=id+"-old.png"
    path=os.path.join('static', 'original-old','')
    path=path+name
    
    original=Image.open(path)
    width,height=original.size
    top=int(t)
    left=int(l)
    right=int(l)+int(w)
    bottom=int(t)+int(h)
    
    #name=img
    #name.replace("\\",'/')
    #name=name.replace("original-old",'cropped-old')
    
    name=name.replace("-old.png","-old-cropped.png")
    path=os.path.join('static', 'cropped-old','')
    path=path+name
    
    #name="demo.png"
    #path = name
    
    cropped=original.crop((left,top,right,bottom))
    #cropped.show()
    cropped.save(path)
 
#cropss("https://www.cbit.ac.in/current_students/exam-time-table/",1067,703,306,512)
