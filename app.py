from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message


app = Flask(__name__)
# app.secret_key="1234567890"

app.config["SESSION_PARMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

dt = datetime.now()
frmt = dt.strftime('%Y-%m-%d')

frmd = dt.strftime('%d %b %Y')
frmtt = dt.strftime('%I:%M%p')
# print(frmt)

d = slice(8, 10)
m = slice(5, 7)
y = slice(0, 4)

dd = frmt[d]
mm = frmt[m]
yyyy = frmt[y]



dmy = dd + "/" + mm + "/" + yyyy
# print(dmy)

class Data(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    food = db.Column(db.String(200), nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    fat = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.user} - {self.food} - {self.calories}"

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=False)
    cal = db.Column(db.Integer, nullable=False)
    pro = db.Column(db.Integer, nullable=False)
    fat = db.Column(db.Integer, nullable=False)
    cab = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.user} - {self.cal} - {self.pro} - {self.fat} - {self.cab}"

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'fitness.buddy2.k22@gmail.com'
app.config['MAIL_PASSWORD'] = 'omjhocxwvrhedfyq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender='fitness.buddy2.k22@gmail.com'
    )
    mail.send(msg)

con=sqlite3.connect("database.db")
con.execute("create table if not exists users(id integer primary key,name text,gender text,age integer, weight integer, height integer, calorie integer,protein integer, carb integer, fat integer, gmail text,username text,password text)")
con.close()

@app.route('/')
def index():
    if not session.get("username"):
        return redirect("/home")
    return redirect("/dashboard")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from users where username=? and password=?",(username,password))
        data=cur.fetchone()
        
        if data:
            session["username"]=data["username"]
            session["password"]=data["password"]
            return redirect("/dashboard")
        else:
            flash("Username and Password Mismatch","red")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            mail=request.form['mail']
            username=request.form['username']
            password=request.form['password']
            html = render_template('temp.html', name=name, username=username, password=password)
            send_email(mail, 'Thank you! For Register in Fitness Buddy.', html)
           
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into users(name,gmail,username,password)values(?,?,?,?)",(name,mail,username,password))
            con.commit()
            con.close()
            flash("Account Created Successfully","green")
        except:
            flash("Something Went Wrong","red")
        finally:
            return redirect(url_for("login"))

    return render_template('register.html')

@app.route('/dashboard',methods=["GET","POST"])
def dashboard():
    if not session.get("username"):
        return redirect("/login")
    return render_template("dashboard.html")

@app.route('/profile',methods=['GET','POST'])
def profile():

    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from users where username=? and password=?",(session["username"],session["password"]))
    profile=cur.fetchone()  
    if request.method=='POST':
        name=request.form['name']
        username=request.form['username']
        password=request.form['password']
        gmail=request.form['gmail']
        age=request.form['age']
        height=request.form['height']
        weight=request.form['weight']

        cur.execute("""update users set name = ?,username = ?,password == ?,age = ?,weight = ?,height = ?,gmail == ? where username = ? and password = ? """,(name,username,password,age,weight,height,gmail, session["username"],session["password"]))
        con.commit()
        con.close()
        return redirect("/profile")
    return render_template("profile.html", profile=profile)

@app.route('/calorie',methods=["GET","POST"])
def calorie():
    if not session.get("username"):
        return redirect("/login")
    if request.method=='POST':
        gender=request.form['gender']
        age=request.form['age']
        weight=request.form['weight']
        height=request.form['height']
        activity=request.form['activity']
        if gender=="male":
            bmr=(10* float (weight))+(6.25*float (height))-(5*float (age))+5
            print(bmr)
        else:
            bmr=(10* float (weight))+(6.25*float (height))-(5*float (age))-161
            print(bmr)

        calorie=round(float(activity)*float(bmr))
        print(calorie)

        pro = round((calorie * 0.4)/4)
        cab = round((calorie * 0.1325)/4)
        fat = round((calorie * 0.676)/9)

        con=sqlite3.connect("database.db")
        cur=con.cursor()
        cur.execute("""update users set gender = ?,age = ?,weight = ?,height = ?,calorie = ?,protein = ?,carb=?,fat=? where username = ? and password = ? """,(gender,age,weight,height,calorie,pro,cab,fat, session["username"],session["password"]))
        con.commit()
        con.close()
        # print(gender,age,weight,height,activity)
        # return render_template("cal_result.html", calorie=calorie, pro=pro, cab=cab, fat=fat)
        return redirect("/macro")
    return render_template("calorie.html")   

@app.route('/macro')
def macro():
    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from users where username=? and password=?",(session["username"],session["password"]))
    data=cur.fetchone()
    cal = data["calorie"]
    pros = data["protein"]
    fats = data["fat"]
    carb = data["carb"]
    return render_template("macro.html", cals=cal, pros=pros, fats=fats, carbs=carb)

@app.route('/logs',methods=["GET","POST"])
def logs():
    if not session.get("username"):
        return redirect("/login")
    if request.method=='POST':
        food = request.form['food']
        protein = request.form['protein']
        fat = request.form['fat']
        carbs = request.form['carbs']
        calories = int(protein)*4+int(fat)*9+int(carbs)*4
        data = Data(user=session["username"], food=food, protein=protein, fat=fat, carbs=carbs, calories=calories, date=frmt)
        db.session.add(data)
        db.session.commit()
    # allData = Data.query.all()

    # allData = Data.query.filter(Data.user == session["username"])
    allData = Data.query.filter(Data.user == session["username"]).filter(Data.date == frmt)
    allCal = allPros = allFats = allCarbs = 0
    for x in allData:
        print(x.calories)
        allCal = allCal + x.calories
        allPros = allPros + x.protein
        allFats = allFats + x.fat
        allCarbs = allCarbs + x.carbs
    print(allCal, allPros, allFats, allCarbs)
    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from users where username=? and password=?",(session["username"],session["password"]))
    data=cur.fetchone()
    cal = data["calorie"]
    pros = data["protein"]
    fats = data["fat"]
    carb = data["carb"]

    color = {
        'yellow': 'e1eb34',
        'green': '02b00d',
        'red': 'fc1703'}

    if allCal < cal:
        calcol = color["red"]
    elif allCal > cal:
        calcol = color["green"]
    else:
        calcol = color["yellow"]

    if allPros < pros:
        procol = color["red"]
    elif allPros > pros:
        procol = color["green"]
    else:
        procol = color["yellow"]

    if allFats < fats:
        fatcol = color["red"]
    elif allFats > fats:
        fatcol = color["green"]
    else:
        fatcol = color["yellow"]

    if allCarbs < carb:
        cabcol = color["red"]
    elif allCarbs > carb:
        cabcol = color["green"]
    else:
        cabcol = color["yellow"]

    return render_template("log.html", allData=allData, date=dmy, allCal=allCal, allPros=allPros, allFats=allFats, allCarbs=allCarbs, cals=cal, pros=pros, fats=fats, carbs=carb, calcol=calcol, procol=procol, fatcol=fatcol, cabcol=cabcol)

@app.route('/view',methods=["GET","POST"])
def view():
    if not session.get("username"):
        return redirect("/login")
    if request.method=='POST':
        view = request.form['view']
        print(view)
        d = slice(8, 10)
        m = slice(5, 7)
        y = slice(0, 4)

        dd = view[d]
        mm = view[m]
        yyyy = view[y]
        dmy = dd + "/" + mm + "/" + yyyy
        print(dmy)
    
    allData = Data.query.filter(Data.user == session["username"]).filter(Data.date == view)
    allCal = allPros = allFats = allCarbs = 0
    for x in allData:
        print(x.calories)
        allCal = allCal + x.calories
        allPros = allPros + x.protein
        allFats = allFats + x.fat
        allCarbs = allCarbs + x.carbs
    print(allCal, allPros, allFats, allCarbs)
    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from users where username=? and password=?",(session["username"],session["password"]))
    data=cur.fetchone()
    cal = data["calorie"]
    pros = data["protein"]
    fats = data["fat"]
    carb = data["carb"]

    color = {
        'yellow': 'e1eb34',
        'green': '02b00d',
        'red': 'fc1703'}

    if allCal < cal:
        calcol = color["red"]
    elif allCal > cal:
        calcol = color["green"]
    else:
        calcol = color["yellow"]

    if allPros < pros:
        procol = color["red"]
    elif allPros > pros:
        procol = color["green"]
    else:
        procol = color["yellow"]

    if allFats < fats:
        fatcol = color["red"]
    elif allFats > fats:
        fatcol = color["green"]
    else:
        fatcol = color["yellow"]

    if allCarbs < carb:
        cabcol = color["red"]
    elif allCarbs > carb:
        cabcol = color["green"]
    else:
        cabcol = color["yellow"]

    return render_template('view.html', allData=allData, date=dmy, allCal=allCal, allPros=allPros, allFats=allFats, allCarbs=allCarbs, cals=cal, pros=pros, fats=fats, carbs=carb, calcol=calcol, procol=procol, fatcol=fatcol, cabcol=cabcol)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        food = request.form['food']
        protein = request.form['protein']
        fat = request.form['fat']
        carbs = request.form['carbs']
        data = Data.query.filter_by(sno=sno).first()
        data.food = food
        data.protein = protein
        data.fat = fat
        data.carbs = carbs
        calories = int(protein)*4+int(fat)*9+int(carbs)*4
        data.calories = calories
        db.session.add(data)
        db.session.commit()
        return redirect("/logs")
    data = Data.query.filter_by(sno=sno).first()
    return render_template('update.html', data=data)

@app.route('/delete/<int:sno>')
def delete(sno):
    data = Data.query.filter_by(sno=sno).first()
    db.session.delete(data)
    db.session.commit()
    return redirect('/logs')

@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    return render_template('bmi.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])

def contact():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        number=request.form['number']
        msg=request.form['msg']
        html = render_template('cont.html', name=name, email=email, number=number, frmd=frmd, frmtt=frmtt, msg=msg)
        send_email(email, 'Thank you! For Contacting Us.', html)
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session["username"] = None
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=False,port=5000)
