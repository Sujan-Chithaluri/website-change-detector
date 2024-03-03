from flask import Flask,render_template,flash,redirect,session
from flask import request
from flask import jsonify
from flask_mysqldb import MySQL
from flask_mail import Mail,Message


from fetch import takess,cropss
from otp import rand_pass
import os

old_ss=os.path.join('static', 'original-old')
crop_old_ss=os.path.join('static', 'cropped-old')


app = Flask(__name__)

app.config['SECRET_KEY'] = '12345'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='sujan@mysql@35'
app.config['MYSQL_DB']='majorproject'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='websitemonitoring2357@gmail.com'
app.config['MAIL_PASSWORD']='Websitemonitoring@2357'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

app.config['UPLOAD_FOLDER_OLD'] = old_ss
app.config['UPLOAD_FOLDER_CROP_OLD'] = crop_old_ss

mail=Mail(app)
mysql=MySQL(app)


@app.route('/')
def index():
    return render_template('login.html')
    
@app.route('/signup')  
def signup():
    return redirect('/')
    
@app.route('/signin')  
def signin():
    return redirect('/')
    
@app.route('/dashboard')  
def dashboard():
    if 'user_id' in session:
        return render_template('layout.html')
    else :
        flash("Please login to continue",'danger') 
        return redirect('/')

@app.route('/signin',methods = ['POST', 'GET'])  
def signin_post():
    if request.method == 'POST':
        uemail=request.form['lemail']
        upass=request.form['lpass']

        cur=mysql.connection.cursor()
        cur.execute("select * from user where lemail=%s and lpassword=%s",(uemail,upass))
        users=cur.fetchall()
        
        #print(users)
        
        if len(users)>0:
            session['user_id']=users[0][0]
            session['user_name']=users[0][1]
            session['user_emailid']=users[0][3]
            session['isadmin']=users[0][4]
            
            return redirect('/dashboard')
            
        else:
            flash("Invalid Credentials",'danger') 
            return redirect('/signin')


@app.route('/signup',methods = ['POST', 'GET'])  
def signup_post():
    if request.method == 'POST':
        # uname=request.form['userName']
        # upass1=request.form['pass1']
        # upass2=request.form['pass2']
        # emailid=request.form['emailAdd']
        
        session['temp_uname']=request.form['userName']
        session['temp_upass']=request.form['pass1']
        session['temp_emailid']=request.form['emailAdd']
        
        cur=mysql.connection.cursor()
        cur.execute("select * from user where lemail=%s " ,(session['temp_emailid'],))
        mails=cur.fetchall()
        
        if len(mails)>0:
            flash("Account already exists with this EMAIL ADDRESS",'danger')
            return render_template('login.html')
       
        else:
          
            st1=rand_pass()
            session['user_otp']=st1
            msg=Message(subject='Confirmation Code', sender='websitemonitoring2357@gmail.com',recipients=[session['temp_emailid']])
            msg.body="Your confirmation code for the Websitemonitoring Account is \n"+st1
            mail.send(msg)
            
            #flash("Successfully Registered",'info')
            
        cur.close()
        return redirect('/validate')

@app.route('/validate')  
def validate():   
    return render_template('validate.html')

@app.route('/verify',methods=['GET','POST'])  
def verify():    
    if request.method == 'POST':
        if request.form.get("s1"):
            st1=rand_pass()
            session['user_otp']=st1
            msg=Message(subject='Confirmation Code', sender='websitemonitoring2357@gmail.com',recipients=[session['temp_emailid']])
            msg.body="Your confirmation code for the Websitemonitoring Account is \n"+st1
            mail.send(msg)
            flash("Check your new confirmation code",'info')
            return render_template('validate.html')
        
        if request.form.get("s2"):
            
            otp=request.form['otp']
            
            if session['user_otp']==otp:
            
                cur=mysql.connection.cursor()
                cur.execute("INSERT INTO user(lname,lpassword,lemail) values (%s,%s,%s)",(session['temp_uname'],session['temp_upass'],session['temp_emailid']))
                mysql.connection.commit()
                
                session.pop('temp_uname')
                session.pop('temp_upass')
                session.pop('temp_emailid')
                session.pop('user_otp')
                    
                flash("Successfully Registered",'info')
                return redirect('/signin')
            
            else:
            
                flash("Invalid Code",'danger')
                return render_template('validate.html')

@app.route('/sendurl',methods = ['POST', 'GET'])  
def sendurl():
    if request.method == 'POST':
        input=request.form['url']
        session['task_url']=input
        try:
            id=takess(input)
            session['uuid']=id
        except:
            flash('There is something wrong with the URL')
            return render_template('frontend.html')
        fullname = os.path.join(app.config['UPLOAD_FOLDER_OLD'],id+"-old.png")
        return render_template('frontend1.html',screenshot=fullname)


@app.route('/sendparam',methods = ['POST', 'GET'])  
def sendparam():
    if request.method == 'POST':
        
        t=int(request.form['t'])
        l=int(request.form['l'])
        w=int(request.form['w'])
        h=int(request.form['h'])
        
        title=request.form['tasktitle']
        kp=request.form['taskkp']
        freq=request.form['taskfreq']
        sens=request.form['tasksens']
        
        url=session['task_url']
        emailid=session['user_emailid']
        uid=session['uuid']
        
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO tasks(taskurl,taskname,taskfreq,tasksens,taskkp,taskemail,imgtop,imgleft,imgwidth,imgheight,imgname) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(url,title,freq,sens,kp,emailid,t,l,w,h,uid))
        mysql.connection.commit()
        cur.close()
        
        cropss(uid,t,l,w,h)
        
        session.pop('uuid')
        session.pop('task_url')
        
        return render_template('frontend.html')


@app.route('/settings')
def settings():
    if 'user_id' in session:
        return render_template('settings.html')
    else :
        flash("Please login to continue",'danger') 
        return redirect('/')
    
@app.route('/changepass',methods = ['POST', 'GET'])
def changepass():
    if 'user_id' in session:
        oldpass=request.form['opass']
        newpass=request.form['pass1']
        
        cur=mysql.connection.cursor()
        cur.execute("select * from user where lemail=%s",(session['user_emailid'],))
        users=cur.fetchall()
        
        if len(users)>0 and oldpass==users[0][2]:
            flash("Password changed successfully",'info')
            
            cur=mysql.connection.cursor()
            cur.execute("UPDATE user SET lpassword=%s where lemail=%s",(newpass,session['user_emailid']))
            mysql.connection.commit()
            cur.close()  
            
            return redirect('/settings')
            
        else:
            flash("Invalid old password",'danger') 
            return redirect('/settings')

    else :
        flash("Please login to continue",'danger') 
        return redirect('/')


@app.route('/viewtasks')
def viewtasks():
    if 'user_id' in session:
        useremail=session['user_emailid']
   
        cur=mysql.connection.cursor()
        cur.execute("select * from tasks where taskemail like %s order by createdDate desc",(useremail,))
        tasks=cur.fetchall()
        
        #print(tasks)
        
        cur.close()
        
        return render_template('viewtasks.html',tasks=tasks)
    else :
        flash("Please login to continue",'danger') 
        return redirect('/')
    
@app.route('/delete/<int:y>')
def deleteTask(y):
        
        id=y
        useremail=session['user_id']
        mysql.connection.commit()

        cur=mysql.connection.cursor()
        cur.execute("delete from tasks where taskid=%s",(id,))
        mysql.connection.commit()
        
        return redirect('/viewtasks')
        
@app.route('/update/<int:y>',methods=['GET','POST'])
def updateTask(y):
        
        id=y
        useremail=session['user_id']
        mysql.connection.commit()

        cur=mysql.connection.cursor()
        cur.execute("select * from tasks where taskid =%s",(id,))
        task=cur.fetchall()
        
        if request.method == 'POST':
            title=request.form['tasktitle']
            kp=request.form['taskkp']
            freq=request.form['taskfreq']
            sens=request.form['tasksens']

            cur=mysql.connection.cursor()
            cur.execute("UPDATE tasks SET taskname=%s, taskkp=%s,taskfreq=%s,tasksens=%s where taskid=%s",(title,kp,freq,sens,id))
            mysql.connection.commit()
            cur.close()  
            return redirect('/viewtasks')
            
        else:
            return render_template('update.html',task=task)

@app.route('/viewlog')
def viewlog():
    if 'user_id' in session:
        return render_template('comparison.html')
    else :
        #flash("Please login to continue",'danger') 
        return render_template('comparison.html')

@app.route('/manageusers')
def manageusers():
    if 'user_id' not in session:
        flash("Please login to continue",'danger') 
        return redirect('/')
    else :
        if session['isadmin']==0:
            return render_template('404.html'), 404
        else:
        
            cur=mysql.connection.cursor()
            cur.execute("select * from user where isadmin=0")
            users=cur.fetchall()

            print(users)
            cur.close()
            return render_template('admin.html',users=users)

@app.route('/deleteuser/<int:y>')
def deleteuser(y):
    if 'user_id' not in session:
            flash("Please login to continue",'danger') 
            return redirect('/')
    else :
            
        if session['isadmin']==0:
            return render_template('404.html'), 404
        else:
            id=y
  
            cur=mysql.connection.cursor()
            cur.execute("select * from user where uid=%s",(id,))
            user=cur.fetchall()
            
            cur=mysql.connection.cursor()
            cur.execute("delete from user where uid=%s",(id,))
            mysql.connection.commit()
            
            cur=mysql.connection.cursor()
            cur.execute("delete from tasks where taskemail=%s",(user[0][3],))
            mysql.connection.commit()
            
            return redirect('/manageusers')                      

@app.route('/home')
def profile():
    if 'user_id' in session:
        return render_template('frontend.html')
    else :
        flash("Please login to continue",'danger') 
        return redirect('/')



@app.route('/logout')  
def logout():
    if 'user_id' in session:
        session.pop('user_id')
        session.pop('user_name')
        session.pop('user_emailid')
        session.pop('isadmin')
        return redirect('/signup')
    else :
        flash("Please login to continue",'danger') 
        return redirect('/')
        
@app.errorhandler(404)
def page_not_found(e):
    if 'user_id' in session:
        return render_template('404.html'), 404
    else :
        flash("Please login to continue",'danger') 
        return redirect('/')
        
if __name__ == '__main__':
    app.run(debug=True)