from flask import Flask,render_template,url_for,request
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
from statistics import mean
from pymongo import MongoClient
import datetime

client= MongoClient('localhost',27017)

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'LynyrdSkynyrd'
app.config['MYSQL_DB'] = 'hospmgmt'
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'annetteshajan@gmail.com',
	MAIL_PASSWORD = 'LynyrdSkynyrd'
	)
mail = Mail(app)
mysql = MySQL(app)
with app.app_context():
    cur = mysql.connection.cursor()


val=''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        details = request.form
        uname = details['username']
        pword = details['password']
        print(uname,pword)
        cur=mysql.connection.cursor()
        cur.execute('''SELECT * FROM ADMIN WHERE USERNAME=%s AND PASSWORD=%s;''',(uname,pword))
        rv=cur.fetchall()
        print ('rv',rv) 
        currentadmin=rv
        global val
        if rv != (): 
            val=currentadmin      
            mysql.connection.commit()
            cur.close()
            return render_template('adminlog.html',val=val)
        cur.execute('''SELECT * FROM PATIENT WHERE USERNAME=%s AND PASSWORD=%s;''',(uname,pword))
        rv=cur.fetchall()
        currentpatient=rv
        print(currentpatient)
        if rv != ():     
            val=currentpatient  
            mysql.connection.commit()
            cur.close()
            return render_template('patientlog.html',val=val)

        cur.execute('''SELECT * FROM DOCTOR WHERE USERNAME=%s AND PASSWORD=%s;''',(uname,pword))
        rv=cur.fetchall()
        currentdoctor=rv
        if rv != (): 
            val=currentdoctor    
            print('val=',val)  
            mysql.connection.commit()
            cur.close()
            return render_template('doctorlog.html',val=val)
        
        cur.execute('''SELECT * FROM STAFF WHERE USERNAME=%s AND PASSWORD=%s;''',(uname,pword))
        rv=cur.fetchall()
        currentstaff=rv
        if rv != (): 
            val=currentstaff      
            mysql.connection.commit()
            cur.close()
            return render_template('stafflog.html',val=val)
        
    return render_template('login.html',val=val)
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html',val=val)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    '''
    msg = Message("Forgot Password - AA Healthcare",
  sender="p@gmail.com",
  recipients=[email_addr])
msg.body = 'Hello '+username+',\nYou or someone else has requested that a new password be generated for your account. If you made this request, then please follow this link:'+link
msg.html = render_template('/mails/reset-password.html', username=username, link=link)
mail.send(msg)'''
    return render_template('forgotpwd.html')

@app.route('/resetpwd',methods=['GET','POST'])
def resetpwd():
    global val
    return render_template('resetpwd.html',val=val)

@app.route('/reset',methods=['GET','POST'])
def reset():
    p=request.form["password"]
    confirm=request.form["confirm"]
    if p==confirm:
        global val
        cur = mysql.connection.cursor()

        if val[0][0][0]=='P':
            cur.execute('''UPDATE PATIENT SET PASSWORD=%s WHERE PATIENT_ID=%s''',(p,val[0][0],))
            mysql.connection.commit()
            cur.close()
            return render_template('patientlog.html',val=val)
        elif val[0][0][0]=='D':
            cur.execute('''UPDATE DOCTOR SET PASSWORD=%s WHERE DOCTOR_ID=%s''',(p,val[0][0],))
            mysql.connection.commit()
            cur.close()
            return render_template('doctorlog.html',val=val)
        elif val[0][0][0]=='S':
            cur.execute('''UPDATE STAFF SET PASSWORD=%s WHERE STAFF_ID=%s''',(p,val[0][0],))
            mysql.connection.commit()
            cur.close()
            return render_template('stafflog.html',val=val)
    else:
        return render_template('resetpwd.html',val=val)


@app.route('/patient',methods=['GET','POST'])
def patient():
    addpatient()
    global val
    return render_template('addpatient.html',item=(),val=val)
  
  
@app.route('/addpatient',methods=['GET','POST'])
def addpatient():
    print("Entered")
    
    try:    
        print("try enter")
        fname = request.form['FN']
        lname = request.form['LN']
        print('error1')
        username = request.form['uname']
        print('error1')
        password = request.form['password']
        print('error1')
        dob = request.form['dob']
        email = request.form['email']
        sex = request.form['gender']
        if sex=='male':
            sex='m'
        elif sex=='female':
            sex='f'
        else:
            sex='o'
        height = request.form['height']
        print(height+'ht')
        weight = request.form['weight']
        print(weight)
        bp = request.form['BP']
        hist = request.form['hist']
        phone = request.form['Phone']
        emg_ph = request.form['emerg']
        address = request.form['address']
        print ("Registered")
        cur = mysql.connection.cursor()
        cur.execute('''SELECT COUNT(*) FROM PATIENT''')
        count=cur.fetchall()
        print(count)
        count='P'+str(count[0][0])

        query_string = "SELECT PATIENT_ID FROM PATIENT WHERE USERNAME = %s"
        cur.execute(query_string, (username,))
        rv=cur.fetchall()
        if (rv!=()):
            count=rv[0][0]
            cur.execute('''DELETE FROM PATIENT WHERE PATIENT_ID = %s ''', (count,))
        cur.execute('''SELECT * FROM PATIENT WHERE USERNAME=%s ''',(username,))
        rv= cur.fetchall()
        cur.execute('''INSERT INTO PATIENT(PATIENT_ID,FN,LN,SEX,EMAIL,HEIGHT,WEIGHT,DOB,BP,HISTORY,PHONE,EMERGENCY,ADDRESS,USERNAME,PASSWORD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (count,fname,lname,sex,email,height,weight,dob,bp,hist,phone,emg_ph,address,username,password))        
        mysql.connection.commit()
        print ("Registered")
        cur.close()
        global val
        print("this is val:",val)       
        return render_template('adminlog.html', val=val)
    except Exception as e:
       return(str(e))

@app.route('/doctor',methods=['GET','POST'])
def doctor():
    adddoctor()
    global val
    return render_template('adddoc.html',item=(),val=val)

@app.route('/adddoctor',methods=['GET','POST'])
def adddoctor():
    print('enter doc')
    try:    
        print("try enter")
        fname = request.form['FN']
        print('something')
        lname = request.form['LN']
        password = request.form['password']
        username = request.form['uname']
        email = request.form['email']
        print('somethingelse')
        sex = request.form['gender']
        if sex=='male':
            sex='m'
        elif sex=='female':
            sex='f'
        else:
            sex='o'
        dept= request.form['dep']
        print ('dept=',dept)
        cur=mysql.connection.cursor()   
        q1 = request.form['qual1']
        q2 = request.form['qual2']
        phone = request.form['Phone']
        q3 = request.form['qual3']
        address = request.form['address']
        time1=request.form['time1']
        time2=request.form['time2']
        cur.execute('''SELECT COUNT(*) FROM DOCTOR''')
        count=cur.fetchall()
        print (count)
        count='D'+str(count[0][0])
        query_string = "SELECT DOCTOR_ID FROM DOCTOR WHERE USERNAME = %s"
        cur.execute(query_string, (username,))
        rv=cur.fetchall()
        if (rv!=()):
            count=rv[0][0]
            cur.execute('''DELETE FROM DOCTOR WHERE DOCTOR_ID = %s ''', (count,))
        
        cur.execute('''INSERT INTO DOCTOR(DOCTOR_ID,FN,LN,SEX,EMAIL,DEP_ID,QUAL1,QUAL2,QUAL3,CONSULT,CONSULT_TILL,PHONE,ADDRESS,USERNAME,PASSWORD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (count,fname,lname,sex,email,dept,q1,q2,q3,time1,time2,phone,address,username,password))       
        mysql.connection.commit()
        cur.close()
        print ("Registered")
        cur.close()
        global val
        print('val=',val)
        return render_template('adminlog.html', val=val)
    except Exception as e:
        print('error')
        return(str(e))

@app.route('/staff',methods=['GET','POST'])
def staff():
    addstaff()
    global val
    return render_template('addstaff.html',item=(),val=val)

@app.route('/addstaff',methods=['GET','POST'])
def addstaff():
    print('enter doc')
    try:    
        print("try enter")
        fname = request.form['FN']
        print('something')
        lname = request.form['LN']
        password = request.form['password']
        username = request.form['uname']
        email = request.form['email']
        print('somethingelse')
        dept= request.form['dep']
        print ('dept=',dept)
        cur=mysql.connection.cursor()   
        phone = request.form['Phone']
        cur.execute('''SELECT COUNT(*) FROM STAFF''')
        count=cur.fetchall()
        print (count)
        count='S'+str(count[0][0])
        query_string = "SELECT STAFF_ID FROM STAFF WHERE USERNAME = %s"
        cur.execute(query_string, (username,))
        rv=cur.fetchall()
        if (rv!=()):
            count=rv[0][0]
            cur.execute('''DELETE FROM STAFF WHERE STAFF_ID = %s ''', (count,))
        
        cur.execute('''INSERT INTO STAFF(STAFF_ID,FN,LN,EMAIL,DEP_ID,PHONE,USERNAME,PASSWORD) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''', (count,fname,lname,email,dept,phone,username,password))       
        mysql.connection.commit()
        cur.close()
        print ("Registered")
        cur.close()
        global val
        return render_template('adminlog.html', val=val)
    except Exception as e:
        print('error')
        return(str(e))

@app.route('/admin',methods=['GET','POST'])
def admin():
    addadmin()
    global val
    return render_template('addadmin.html',item=(),val=val)
  
  
@app.route('/addadmin',methods=['GET','POST'])
def addadmin():
    print("Entered")
    
    try:    
        print("try enter")
        fname = request.form["FN"]
        lname = request.form["LN"]
        password = request.form["password"]
        username = request.form["uname"]
        email = request.form["email"]
        phone = request.form["Phone"]
        cur = mysql.connection.cursor()
        cur.execute('''SELECT COUNT(*) FROM ADMIN''')
        count=cur.fetchall()
        print(count)
        count='A'+str(count[0][0])

        query_string = "SELECT ADMIN_ID FROM ADMIN WHERE USERNAME = %s"
        cur.execute(query_string, (username,))
        rv=cur.fetchall()
        if (rv!=()):
            count=rv[0][0]
            cur.execute('''DELETE FROM ADMIN WHERE ADMIN_ID = %s ''', (count,))
        
        cur.execute('''INSERT INTO ADMIN(ADMIN_ID,FN,LN,EMAIL,PHONE,USERNAME,PASSWORD) VALUES (%s,%s,%s,%s,%s,%s,%s)''', (count,fname,lname,email,phone,username,password))        
        mysql.connection.commit()
        print ("Registered")
        cur.close()
        global val
        return render_template('adminlog.html', val=val)
    except Exception as e:
       return(str(e))


@app.route('/upatient',methods=['GET','POST'])
def upatient():
    updatepatient()
    global val
    return render_template("updatepatient.html",val=val)
@app.route('/updatepatient',methods=['GET','POST'])
def updatepatient():
    try:
        print('updating')
        pat_id=request.form['patient_id']
        cur=mysql.connection.cursor()
        print('here')
        query_string = "SELECT DORMANT FROM PATIENT WHERE PATIENT_ID = %s"
        cur.execute(query_string, (pat_id,))
        rv=cur.fetchall()
        global val
        if rv[0][0]==0:
            query_string = "SELECT * FROM PATIENT WHERE PATIENT_ID = %s"
            cur.execute(query_string, (pat_id,))
            mysql.connection.commit()
            rv=cur.fetchall() 
            cur.close()
            print(rv)
            return render_template('addpatient.html',item=rv[0],val=val)
        cur.close()
        return render_template("updatepatient.html",val=val)
        #cur.execute('SELECT * FROM PATIENT WHERE PATIENT_ID = %s', (pat_id))
        
    except Exception as e:
        print('error')
        return(str(e))


@app.route('/udoctor',methods=['GET','POST'])
def udoctor():
    global val
    updatedoctor()
    return render_template("updatedoctor.html",val=val)
@app.route('/updatedoctor',methods=['GET','POST'])
def updatedoctor():
    try:
        print('updating')
        doc_id=request.form['doctor_id']
        cur=mysql.connection.cursor()
        print('here')
        query_string = "SELECT DORMANT FROM DOCTOR WHERE DOCTOR_ID = %s"
        cur.execute(query_string, (doc_id,))
        rv=cur.fetchall()
        global val
        if rv[0][0]==0:
            query_string = "SELECT * FROM DOCTOR WHERE DOCTOR_ID = %s"
            cur.execute(query_string, (doc_id,))
            #cur.execute('SELECT * FROM PATIENT WHERE PATIENT_ID = %s', (pat_id))
            rv=cur.fetchall() 
            mysql.connection.commit()
            cur.close()
            print(rv)
            return render_template('adddoc.html',item=rv[0],val=val)
        cur.close()
        return render_template("updatedoctor.html",val=val)
    except Exception as e:
        print('error')
        return(str(e))

@app.route('/ustaff',methods=['GET','POST'])
def ustaff():
    updatestaff()
    global val
    return render_template("updatestaff.html",val=val)
@app.route('/updatestaff',methods=['GET','POST'])
def updatestaff():
    try:
        print('updating')
        staff_id=request.form['staff_id']
        cur=mysql.connection.cursor()
        print('here')
        query_string = "SELECT DORMANT FROM STAFF WHERE STAFF_ID = %s"
        cur.execute(query_string, (staff_id,))
        rv=cur.fetchall()
        global val
        if rv==():
            return render_template("updatestaff.html", val=val)
        print(rv)
        if rv[0][0]==0:
            query_string = "SELECT * FROM STAFF WHERE STAFF_ID = %s"
            cur.execute(query_string, (staff_id,))
            mysql.connection.commit()
            rv=cur.fetchall() 
            cur.close()
            print(rv)
            return render_template('addstaff.html',item=rv[0],val=val)
        cur.close()
        #return render_template("updatestaff.html")
        #cur.execute('SELECT * FROM PATIENT WHERE PATIENT_ID = %s', (pat_id))
        
    except Exception as e:
        print('error')
        return(str(e))


@app.route('/uadmin',methods=['GET','POST'])
def uadmin():
    updateadmin()
    global val
    return render_template("updateadmin.html",val=val)
@app.route('/updateadmin',methods=['GET','POST'])
def updateadmin():
    try:
        print('updating')
        admin_id=request.form['admin_id']
        cur=mysql.connection.cursor()
        print('here')
        query_string = "SELECT * FROM ADMIN WHERE ADMIN_ID = %s"
        cur.execute(query_string, (admin_id,))
        mysql.connection.commit()
        rv=cur.fetchall() 
        cur.close()
        print(rv)
        global val
        return render_template('addadmin.html',item=rv[0],val=val)
        
        #cur.execute('SELECT * FROM PATIENT WHERE PATIENT_ID = %s', (pat_id))
        
    except Exception as e:
        print('error')
        return(str(e))

@app.route('/dpatient',methods=['GET','POST'])
def dpatient():
    deletepatient()
    global val
    return render_template("deletepatient.html",val=val)
@app.route('/deletepatient',methods=['GET','POST'])
def deletepatient():
    try:
        print('deleting')
        pat_id=request.form['patient_id']
        cur=mysql.connection.cursor()
        print('here',pat_id)
        cur.execute('''SELECT DORMANT FROM PATIENT WHERE PATIENT_ID = %s''', (pat_id,))
        rv=cur.fetchall()
        if rv[0][0]==0:
            cur.execute('''UPDATE PATIENT SET DORMANT=1 WHERE PATIENT_ID = %s''', (pat_id,))
        else:
            cur.execute('''UPDATE PATIENT SET DORMANT=0 WHERE PATIENT_ID = %s''', (pat_id,))

        print('deleted ')
        mysql.connection.commit()
        cur.close()
        global val
        return render_template('adminlog.html',val=val)
    except Exception as e:
        print('error')
        return(str(e))


@app.route('/ddoctor',methods=['GET','POST'])
def ddoctor():
    deletedoctor()
    global val
    return render_template("deletedoctor.html",val=val)
@app.route('/deletedoctor',methods=['GET','POST'])
def deletedoctor():
    try:
        print('deleting')
        doc_id=request.form['doctor_id']
        cur=mysql.connection.cursor()
        print('here')
        cur.execute('''SELECT DORMANT FROM DOCTOR WHERE DOCTOR_ID = %s''', (doc_id,))
        rv=cur.fetchall()
        if rv[0][0]==0:
            cur.execute('''UPDATE DOCTOR SET DORMANT=1 WHERE DOCTOR_ID = %s''', (doc_id,))
        else:
            cur.execute('''UPDATE DOCTOR SET DORMANT=0 WHERE DOCTOR_ID = %s''', (doc_id,))
        cur.close()
        global val
        return render_template('adminlog.html',val=val)
    except Exception as e:
        print('error')
        return(str(e))

@app.route('/dstaff',methods=['GET','POST'])
def dstaff():
    deletestaff()
    global val
    return render_template("deletestaff.html",val=val)
@app.route('/deletestaff',methods=['GET','POST'])
def deletestaff():
    try:
        print('deleting')
        staff_id=request.form['staff_id']
        cur=mysql.connection.cursor()
        print('here')
        cur.execute('''SELECT DORMANT FROM STAFF WHERE STAFF_ID = %s''', (staff_id,))
        rv=cur.fetchall()
        if rv[0][0]==0:
            cur.execute('''UPDATE STAFF SET DORMANT=1 WHERE STAFF_ID = %s''', (staff_id,))
        else:
            cur.execute('''UPDATE STAFF SET DORMANT=0 WHERE STAFF_ID = %s''', (staff_id,))
        cur.close()
        global val
        return render_template('/adminlog',val=val)
    except Exception as e:
        print('error')
        return(str(e))

@app.route('/bookappt',methods=['GET','POST'])
def bookappt():
    bookappt2()
    global val
    print('pat val=',val)
    return render_template("bookappt.html",val=val)

@app.route('/bookappt2',methods=['GET','POST'])
def bookappt2():
    try:
        dep=request.form["dep"]
        cur=mysql.connection.cursor()
        query_string = "SELECT * FROM DOCTOR WHERE DEP_ID = %s"
        cur.execute(query_string, (dep,))
        rv=cur.fetchall()
        cur.close()
        print(rv)
        global val
        print(val)
        book()
        return render_template("bookappt2.html",val2=rv, val=val)
    except Exception as e:
        print('error')
        return(str(e))    

@app.route('/book',methods=['GET','POST'])
def book():
    try:
        doc=request.form["doctor"]
        print(doc)
        cur=mysql.connection.cursor()
        print("here")
        global val
        print (val)
        cur.execute("INSERT INTO APPOINTMENT VALUES(%s,%s)", (doc,val[0][0]))
        mysql.connection.commit()
        cur.close()
        return render_template("patientlog.html",val=val)
    except Exception as e:
        print('error')
        return(str(e))   

@app.route('/viewhistory',methods=['GET','POST'])
def viewhistory():
    
    global val
    cur=mysql.connection.cursor()
    print('val:',val)
    cur.execute('''SELECT DOCTOR_ID,FN,LN FROM DOCTOR D,APPOINTMENT A WHERE A.DOC_ID=D.DOCTOR_ID AND PAT_ID=%s''',(val[0][0],))
    docdetail=cur.fetchall()
    print (docdetail)
    cur.execute('''SELECT * FROM MEDRECORD WHERE PATIENT_ID=%s''',(val[0][0],))
    rec=cur.fetchall()
    if rec==():
        rec=((),)
    cur.execute('''SELECT * FROM ROOM WHERE PATIENT_ID=%s''',(val[0][0],))
    room=cur.fetchall()
    print('room=',room)
    if room==():
        room=((),)
    cur.execute('''SELECT * FROM BILL WHERE PATIENT_ID=%s''',(val[0][0],))
    bill=cur.fetchall()
    if bill==():
        bill=((),)
    cur.close()
    db=client.hospmgmt
    his=db.HISTORY
    if rec!=((),) and bill!=((),) and room!=((),):
        #print(rec[0][2])
        c_date=datetime.datetime.combine(rec[0][2],datetime.datetime.min.time())
        admit=datetime.datetime.combine(room[0][2],datetime.datetime.min.time())
        disch=datetime.datetime.combine(room[0][3],datetime.datetime.min.time())
        fee=int(bill[0][3])
        extra=int(bill[0][4])
        post_data={'PAT_ID':val[0][0],'DOC_ID':docdetail[0][0],'REC_ID':rec[0][0],'C_DATE':c_date,'CASEHIST':rec[0][3],'DIAG':rec[0][4],'PRES':rec[0][5],'FEE':fee,'EXTRA':extra,'ROOM':room[0][0],'ADMIT':admit,'DISCH':disch}
        his=his.insert_one(post_data)
    return render_template("viewhistory.html",item=docdetail[0],rec=rec[0],room=room[0],bill=bill[0],val=val)

@app.route('/rating',methods=['GET','POST'])
def rating():
    rate=request.form["rating"]
    rate=int(rate)
    cur=mysql.connection.cursor()
    global val
    cur.execute('''SELECT DOC_ID FROM APPOINTMENT WHERE PAT_ID=%s''',(val[0][0],))
    doc=cur.fetchall()
    if (rate>=1 and rate<=10):
        cur.execute('''UPDATE DOCTOR SET RATING = %s WHERE DOCTOR_ID = %s''',(rate,doc[0][0],))        
    mysql.connection.commit()
    cur.close()
    return render_template("patientlog.html",val=val)

@app.route('/viewappt',methods=['GET','POST'])
def viewappt():
    try:
        global val
        print('val=',val)
        cur=mysql.connection.cursor()
        cur.execute('''SELECT PATIENT_ID,FN,LN FROM PATIENT P, APPOINTMENT A WHERE A.PAT_ID=P.PATIENT_ID AND A.DOC_ID=%s ''',(val[0][0],))
        rv=cur.fetchall()
        cur.close()
        return render_template("viewappt.html",val=val,val2=rv)
    except Exception as e:
        print('error')
        return(str(e))

@app.route('/diagnosis',methods=['GET','POST'])
def diagnosis():
    try:
        pat_id=request.form['patient_id']
        cur=mysql.connection.cursor()
        global val
        cur.execute('''SELECT PAT_ID,DOC_ID FROM APPOINTMENT WHERE PAT_ID=%s AND DOC_ID=%s''',(pat_id,val[0][0]))
        rv=cur.fetchall()
        if rv!=(()):
            return render_template("diagnosis.html",val=val,item=pat_id)
        cur.execute('''SELECT PATIENT_ID,FN,LN FROM PATIENT P, APPOINTMENT A WHERE A.PAT_ID=P.PATIENT_ID AND A.DOC_ID=%s ''',(val[0][0],))
        rv=cur.fetchall()
        cur.close()
        return render_template("viewappt.html",val=val,val2=rv)

    except Exception as e:
        print('error')
        return(str(e))

@app.route('/updatemedrecord',methods=['GET','POST'])
def updatemedrecord():
    try:
        pat_id=request.form["pat_id"]
        date=request.form["date"]
        symptoms=request.form["symptoms"]
        diagnosis=request.form["diagnosis"]
        presc=request.form["presc"]
        cur=mysql.connection.cursor()
        cur.execute('''SELECT COUNT(*) FROM ADMIN''')
        count=cur.fetchall()
        count='R'+str(count[0][0])
        cur.execute('''INSERT INTO MEDRECORD(RECORD_ID,PATIENT_ID,CONSULT,CASEHIST,DIAGNOSIS,PRESC,DOC_ID) VALUES(%s,%s,%s,%s,%s,%s,%s)''',(count,pat_id,date,symptoms,diagnosis,presc,val[0][0]))
        mysql.connection.commit()
        cur.close()
        return render_template("doctorlog.html",val=val)
    except Exception as e:
        print('error')
        return(str(e))


@app.route('/patientbill',methods=['GET','POST'])
def patientbill():
    global val
    return render_template("patientbill.html",val=val)

@app.route('/bill',methods=['GET','POST'])
def bill():
    pat_id=request.form["pat_id"]
    doc_id=request.form["doc_id"]
    consult=request.form["consultfee"]
    extra=request.form["extra"]
    cur=mysql.connection.cursor()
    cur.execute('''SELECT DOC_ID,PAT_ID FROM APPOINTMENT WHERE DOC_ID=%s AND PAT_ID=%s''',(doc_id,pat_id,))
    rv=cur.fetchall()
    if rv==():
        return render_template("patientbill.html")
    cur.execute('''SELECT COUNT(*) FROM BILL''')
    count=cur.fetchall()
    count='B'+str(count[0][0])
    cur.execute('''INSERT INTO BILL(BILL_ID,PATIENT_ID,DOCTOR_ID,CONSULTFEE,EXTRA) VALUES(%s,%s,%s,%s,%s)''',(count,pat_id,doc_id,consult,extra))
    mysql.connection.commit()
    cur.close()
    global val
    return render_template("stafflog.html",val=val)

@app.route('/inpatient',methods=['GET','POST'])
def inpatient():
    return render_template("inpatient.html",val=val)

@app.route('/room',methods=['GET','POST'])
def room():
    pat_id=request.form["pat_id"]
    doc_id=request.form["doc_id"]
    roomno=request.form["roomno"]
    admit=request.form["admit"]
    discharge=request.form["disch"]
    cur=mysql.connection.cursor()
    cur.execute('''SELECT DOC_ID,PAT_ID FROM APPOINTMENT WHERE DOC_ID=%s AND PAT_ID=%s''',(doc_id,pat_id,))
    rv=cur.fetchall()
    if rv==():
        return render_template("inpatient.html",val=val)

    cur.execute('''INSERT INTO ROOM(ROOM_NO,PATIENT_ID,ADMITDATE,DISCHARGE,DOC_ID,STAFF_ID) VALUES(%s,%s,%s,%s,%s,%s)''',(roomno,pat_id,admit,discharge,doc_id,val[0][0]))
    mysql.connection.commit()
    cur.close()
    return render_template("stafflog.html",val=val)

 
if __name__=="__main__":
    app.run(debug=True)