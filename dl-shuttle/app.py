from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pose
import os
import glob
from datetime import date

app = Flask(__name__)
  
  
app.secret_key = 'abc'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abc60458'
app.config['MYSQL_DB'] = 'coachlogin'
  
mysql = MySQL(app)
UPLOAD_FOLDER = 'Upload Video'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['user_id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s,NULL, NULL)', (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/save_profile', methods =['GET', 'POST'])
def save_profile():
    msg = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    userid = session['id']
    password = request.form['password']
    gender = request.form['gender']
    skill = request.form['skill']
    email = request.form['email']     
    if request.method == 'POST' and password != "":       
        cursor.execute('UPDATE accounts SET password = % s where user_id = %s', (password, userid, ))
    if request.method == 'POST' and gender != "":       
        cursor.execute('UPDATE accounts SET gender = % s where user_id = %s', (gender, userid, ))
    if request.method == 'POST' and skill != "":       
        cursor.execute('UPDATE accounts SET skill = % s where user_id = %s', (skill, userid, ))
    if request.method == 'POST' and email != "":
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
            return render_template('profile.html', msg=msg)     
        cursor.execute('UPDATE accounts SET email = % s where user_id = %s', (email, userid, ))
    mysql.connection.commit()
    return render_template('home.html', msg=msg)

@app.route("/upload_smash_video", methods=["GET", "POST"])
def upload_smash_video():
    files = glob.glob('./Upload Video/*.mp4')
    if request.method == "POST":
        if request.files:
            for f in files:
                os.remove(f)
            video = request.files["video"]
            coverPath = os.path.join( app.config['UPLOAD_FOLDER'], video.filename)
            video.save(coverPath)
            msg = 'Upload Successfull'
            return redirect(request.url)

    return render_template("upload_smash_video.html")

@app.route("/upload_clear_video", methods=["GET", "POST"])
def upload_clear_video():
    files = glob.glob('./Upload Video/*.mp4')
    if request.method == "POST":
        if request.files:
            for f in files:
                os.remove(f)
            video = request.files["video"]
            coverPath = os.path.join( app.config['UPLOAD_FOLDER'], video.filename)
            video.save(coverPath)
            msg = 'Upload Successfull'
            return redirect(request.url)

    return render_template("upload_clear_video.html")

@app.route("/upload_serve_video", methods=["GET", "POST"])
def upload_serve_video():
    files = glob.glob('./Upload Video/*.mp4')
    if request.method == "POST":
        if request.files:
            for f in files:
                os.remove(f)
            video = request.files["video"]
            coverPath = os.path.join( app.config['UPLOAD_FOLDER'], video.filename)
            video.save(coverPath)
            return redirect(request.url)

    return render_template("upload_serve_video.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/tutorial')
def tutorial():
    return render_template("tutorial.html")

@app.route('/guide')
def guide():
    return render_template("guide.html")

@app.route('/guide1')
def guide1():
    return render_template("guide1.html")

@app.route('/guide2')
def guide2():
    return render_template("guide2.html")

@app.route('/clearGuide')
def clearGuide():
    return render_template("clearGuide.html")

@app.route('/smashGuide')
def smashGuide():
    return render_template("smashGuide.html")

@app.route('/serveGuide')
def serveGuide():
    return render_template("serveGuide.html")

@app.route('/skill_selection')
def skill_selection():
    return render_template('skill_selection.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/history')
def history():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    dbuserid = session['id']
    cursor.execute('SELECT * FROM training_records WHERE user_id = % s and training_id = 2', (dbuserid, ))
    account = cursor.fetchone()
    date1 = account['training_date']
    skill1 = account['technique']
    CP1 = account['correct_pose']
    IP1 = account['incorrect_pose']
    cursor.execute('SELECT * FROM training_records WHERE user_id = % s and training_id = 3', (dbuserid, ))
    account = cursor.fetchone()
    date2 = account['training_date']
    skill2 = account['technique']
    CP2 = account['correct_pose']
    IP2 = account['incorrect_pose']
    cursor.execute('SELECT * FROM training_records WHERE user_id = % s and training_id = 4', (dbuserid, ))
    account = cursor.fetchone()
    date3 = account['training_date']
    skill3 = account['technique']
    CP3 = account['correct_pose']
    IP3 = account['incorrect_pose']
    return render_template('history.html', date2 = date2, skill1 = skill1, CP1 = CP1, IP1 = IP1, 
    date1 = date1, skill2 = skill2, CP2 =CP2, IP2=IP2, date3 = date3, skill3 = skill3, CP3 =CP3, IP3=IP3)

@app.route('/summary')
def summary():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    dbuserid = session['id']
    dbusername = session['username']
    cursor.execute('SELECT SUM(correct_pose) FROM training_records WHERE user_id = % s AND technique = "clear";', (dbuserid, ))
    account = cursor.fetchone()
    TotalCPClear = account['SUM(correct_pose)']
    cursor.execute('SELECT SUM(incorrect_pose) FROM training_records WHERE user_id = % s AND technique = "clear";', (dbuserid, ))
    account = cursor.fetchone()
    TotalIPClear = account['SUM(incorrect_pose)']
    cursor.execute('SELECT SUM(correct_pose) FROM training_records WHERE user_id = % s AND technique = "smash";', (dbuserid, ))
    account = cursor.fetchone()
    TotalCPSmash = account['SUM(correct_pose)']
    cursor.execute('SELECT SUM(incorrect_pose) FROM training_records WHERE user_id = % s AND technique = "smash";', (dbuserid, ))
    account = cursor.fetchone()
    TotalIPSmash = account['SUM(incorrect_pose)']
    cursor.execute('SELECT SUM(correct_pose) FROM training_records WHERE user_id = % s AND technique = "serve";', (dbuserid, ))
    account = cursor.fetchone()
    TotalCPServe = account['SUM(correct_pose)']
    cursor.execute('SELECT SUM(incorrect_pose) FROM training_records WHERE user_id = % s AND technique = "serve";', (dbuserid, ))
    account = cursor.fetchone()
    TotalIPServe = account['SUM(incorrect_pose)']
    clearSum = TotalCPClear + TotalIPClear
    smashSum = TotalCPSmash + TotalIPSmash
    serveSum = TotalCPServe + TotalIPServe
    return render_template('summary.html', name=dbusername, clearCP=TotalCPClear, clearIP=TotalIPClear, 
    smashCP=TotalCPSmash, smashIP=TotalIPSmash, serveCP=TotalCPServe, serveIP=TotalIPServe, clear=clearSum,smash=smashSum,serve=serveSum)

@app.route('/view_smash_pose')
def view_smash_pose():
    if os.path.exists('./static/Image/Smash/WrongPose0.jpg' and './static/Image/Smash/WrongPose1.jpg'):
        return render_template('view_smash_IP.html')
    else:
        return render_template('view_smash_CP.html')

@app.route('/view_clear_pose')
def view_clear_pose():
    if os.path.exists('./static/Image/Clear/WrongPose0.jpg' and './static/Image/Clear/WrongPose1.jpg'):
        return render_template('view_clear_IP.html')
    else:
        return render_template('view_clear_CP.html')

@app.route('/view_serve_pose')
def view_serve_pose():
    if os.path.exists('./static/Image/Serve/WrongPose0.jpg' and './static/Image/Serve/WrongPose1.jpg'):
        return render_template('view_serve_IP.html')
    else:
        return render_template('view_serve_CP.html')

@app.route('/smash', methods=["GET", "POST"])
def smash():
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    dbuserid = session['id']
    correctPose,incorrectPose,counter = pose.poseEstimationSmash()
    cursor.execute('INSERT INTO training_records VALUES (NULL, % s, % s, % s, % s, % s, % s)', (dbuserid, today, 'smash', correctPose, counter, incorrectPose))
    mysql.connection.commit()
    percentCP = (correctPose/counter)*100
    percentCP = float("{:.2f}".format(percentCP))
    percentIP = 100 - percentCP
    percentIP = float("{:.2f}".format(percentIP))
    if percentCP>=80:
        comment = "Your basic smashing skill is great. Now try to train for jumping smash, because jumping will give your a higher hitting point and make your smash steeper. Opponents takes more effort in defending such smash."
    elif percentCP<80 and percentCP>60:
        comment = "Your smash is inconsistent, some of your smash are inappropriate. A bad smash will cause you in disadvantages causing you to lose marks. Make sure your hitting point are high enough and your left hand need to strech out in preparation and support your body. Finally after your smash, let your swing follow to the lower left of your body."
    elif percentCP<=60:
        comment = "Your smashing skill is poor, brush up more and observe how good players doing a smash. Make sure your hitting point are high enough and your left hand need to strech out in preparation and support your body. Finally after your smash, let your swing follow to the lower left of your body."
    return render_template("smash.html", count=counter,CP=correctPose,IP=incorrectPose,Date=d2,perCP=percentCP,perIP=percentIP, cmt=comment)

@app.route('/clear', methods=["GET", "POST"])
def clear():
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    dbuserid = session['id']
    correctPose,incorrectPose,counter = pose.poseEstimationClear()
    cursor.execute('INSERT INTO training_records VALUES (NULL, % s, % s, % s, % s, % s, % s)', (dbuserid, today, 'clear', correctPose, counter, incorrectPose))
    mysql.connection.commit()
    percentCP = (correctPose/counter)*100
    percentCP = float("{:.2f}".format(percentCP))
    percentIP = 100 - percentCP
    percentIP = float("{:.2f}".format(percentIP))
    if percentCP>=80:
        comment = "Your basic clear skill are up to standard! Now enhance your clear skill by playing clear from different part of the court and make sure it reach the baseline on the other side of the court. Playing a good clear give you a short amount of time to rest and prepare for the next short."
    elif percentCP<80 and percentCP>60:
        comment = "Some of your clear is incorrect. Your left hand need to stretch up to support your body when hitting the shuttle. While your shoulder should lift up high to have a high hitting point"
    elif percentCP<=60:
        comment = "You have to brush up on your clear skill, it is the most import basic skill in badminton. When hitting a clear your left hand need to stretch up to support your body when hitting the shuttle. While your shoulder should lift up high to have a high hitting point."
    return render_template('clear.html', count=counter,CP=correctPose,IP=incorrectPose,Date=d2,perCP=percentCP,perIP=percentIP,cmt=comment)

@app.route('/serve', methods=["GET", "POST"])
def serve():
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    dbuserid = session['id']
    correctPose,incorrectPose,counter = pose.poseEstimationServe()
    cursor.execute('INSERT INTO training_records VALUES (NULL, % s, % s, % s, % s, % s, % s)', (dbuserid, today, 'serve', correctPose, counter, incorrectPose))
    mysql.connection.commit()
    percentCP = (correctPose/counter)*100
    percentCP = float("{:.2f}".format(percentCP))
    percentIP = 100 - percentCP
    percentIP = float("{:.2f}".format(percentIP))
    if percentCP>=80:
        comment = "Your serving skill are quite good, you can move on to try and serve to different corner of the courts. This will give you a high advantage in giving your opponents pressure."
    elif percentCP<80 and percentCP>60:
        comment = "Some of your serve may be fault as a correct serve cannot be higher than your waist, takes note and improve from that"
    elif percentCP<=60:
        comment = "You have to brush up on your serving skill, and make sure your serving point of your shuttle cannot be higher than your waist"
    return render_template('serve.html', count=counter,CP=correctPose,IP=incorrectPose,Date=d2,perCP=percentCP,perIP=percentIP, cmt=comment)    

def __init__(self, path = '/Users/chai1/Desktop/Web/login/main.py'):
    self.path = path

if __name__ == '__main__':
    app.run(debug=True)