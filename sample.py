import mysql.connector
import datetime
import pandas
import time
from datetime import datetime

import schedule
import time

def dummy():
    print("Hello Sujan")

schedule.every(1).minutes.do(dummy)


while True:
    schedule.run_pending()
    time.sleep(1)

# mydb = mysql.connector.connect(
  # host="localhost",
  # user="root",
  # password="sujan@mysql@35",
  # database="majorproject"
# )

# now = datetime.now()
# mycursor = mydb.cursor()
# mycursor.execute("SELECT * FROM tasks ")
# #mycursor.execute("SELECT * FROM tasks where nextcheck=NULL or nextcheck<%s",(now,))
# myresult = mycursor.fetchall()

# now = datetime.now()

# for x in myresult:
    # print(x[13])

# # 15 mins
# # 30 mins
# # 1 hour
# # 3 hours
# # 6 hours
# # 1 day
# # 1 week

# print("before rounding :\t",now)

# temp=pandas.Series(now).dt.ceil('15min')[0]
# print("After rounding to 15 mins :\t",temp)

# temp=pandas.Series(now).dt.ceil('30min')[0]
# print("After rounding to 30mins :\t",temp)

# temp=pandas.Series(now).dt.ceil('1H')[0]
# print("After rounding to 1 hour :\t",temp)

# temp=pandas.Series(now).dt.ceil('3H')[0]
# print("After rounding to 3 hours :\t",temp)
        
# temp=pandas.Series(now).dt.ceil('6H')[0]
# print("After rounding to 6 hours :\t",temp)  

# temp=pandas.Series(now).dt.ceil('1D')[0]
# temp=temp+pandas.DateOffset(hours=9)
# print("After rounding to 1 day :\t",temp)

# temp=pandas.Series(now).dt.ceil('7D')[0]
# temp=temp+pandas.DateOffset(hours=9)
# print("After rounding to 1 week:\t",temp)
        
# for x in myresult:

    # if x[3]=="15 mins":
        # temp=pandas.Series(now).dt.ceil('15min')[0]
       
        # mycursor = mydb.cursor()
        # mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        # mydb.commit()
    
    # if x[3]=="30 mins":
        # temp=pandas.Series(now).dt.ceil('30min')[0]
        
        # mycursor = mydb.cursor()
        # mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        # mydb.commit()
   
    # if x[3]=="1 hour":
        # temp=pandas.Series(now).dt.ceil('1H')[0]
        
        # mycursor = mydb.cursor()
        # mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        # mydb.commit()
   
    # if x[3]=="3 hours":
        # temp=pandas.Series(now).dt.ceil('3H')[0]
        
        # mycursor = mydb.cursor()
        # mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        # mydb.commit()

    # if x[3]=="6 hours":
        # temp=pandas.Series(now).dt.ceil('6H')[0]
        
        # mycursor = mydb.cursor()
        # mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        # mydb.commit()


    # if x[3]=="1 day":
        # temp=pandas.Series(now).dt.ceil('1D')[0]
        # temp=temp+pandas.DateOffset(hours=9)
        
        # mycursor = mydb.cursor()
        # mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        # mydb.commit()
        

    # if x[3]=="1 week":
        # temp=pandas.Series(now).dt.ceil('7D')[0]
        # temp=temp+pandas.DateOffset(hours=9)
      
        # mycursor = mydb.cursor()
        # mycursor.execute("UPDATE tasks set nextCheck = %s where taskid=%s",(temp,x[0]))
        # mydb.commit()        