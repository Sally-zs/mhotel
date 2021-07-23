# -*- coding: utf-8 -*-
#coding:utf-8
from operator import itemgetter
from flask import Flask,render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import datetime
from functools import wraps



def query_user(user_id):
    for user in users:
        if user_id == user['id']:
            return user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Kyven@123@121.4.38.213:3306/shumei?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_ECHO'] = True  #执行过的sql会打印出来
app.config["SECRET_KEY"] = '127997080'
db =  SQLAlchemy(app)
#新建用户表
class User(db.Model):
    __tablename__= "user"
    userid = db.Column(
        "userid",db.Integer,
        primary_key=True,
        autoincrement = True
    )
    username =db.Column(
     "username",db.String(10)
    )
    pwd = db.Column(
        "pwd",db.Integer
    )
#新建用户信息表
class User_info(db.Model):
    __tablename__= "user_info"
    userid = db.Column(
        "userid",db.Integer,
        primary_key=True,
        autoincrement = True
    )
    phone =db.Column(
     "phone",db.String(20)
    )
    card_id = db.Column(
        "card_id",db.String(20)
    )
    address = db.Column(
        "address",db.String(20)
    )




#新建房间表
class Room(db.Model):
    __tablename__= "room"
    roomid = db.Column(
        "roomid",db.Integer,
        primary_key=True,
        autoincrement = True
    )
    type = db.Column(
        "type",db.String(10)
    )
    price = db.Column(
        "price",db.Integer
    )

#新建订单表
class Order(db.Model):
    __tablename__= "order"
    orderid = db.Column(
        "orderid",db.Integer,
        primary_key=True,
        autoincrement = True
    )
    userid = db.Column(
        "userid",db.Integer,db.ForeignKey('user.userid')
    )
    roomid = db.Column(
        "roomid",db.Integer,db.ForeignKey('room.roomid')
    )
    ordertime = db.Column(
        "ordertime",db.DateTime
    )


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column("id",db.Integer,primary_key=True,autoincrement=True)
    name = db.Column("name",db.String(32))
    def __repr__(self):
        return "<id:{}, name:{}>".format(self.id,self.name)
class Course(db.Model):
    __tablename__ = "course"
    id= db.Column("id",db.Integer,primary_key=True,autoincrement=True)
    name = db.Column("name",db.String(32))
    desc = db.Column("desc",db.String(100))
    students = db.relationship("Student",secondary="student_course_relaiton",backref="courses")
    def __repr__(self):
        return "<id:{}, name:{}, desc:{}>".format(self.id,self.name,self.desc)
studentCourseRelation = db.Table(
    "student_course_relaiton",
    db.Column("student_id",db.ForeignKey("student.id")),
    db.Column("course_id",db.ForeignKey("course.id"))
)
course = Course.query.filter(Course.name == "English").first()
name = Student.query.filter(Student.name == "zhangsan1").all()

print(name)
print(name[0])

# print(course.students)
# print(course.students[0].courses)
db.create_all()

def checkLogin(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get("username"):
            # print("there is sesseion with key username")
            ret = func(*args, **kwargs)  # func = home
            return ret
        else:
            # print("there is not sesseion with key username")
            return redirect("/login")
    return inner


@app.route('/login',methods=("post","get"))
def login():
    if request.method=='POST':
         username = request.form.get("username")
         password=request.form.get('password')
         password = int(password)
         user = User.query.filter(User.username == username , User.pwd == password).first()
         if user!=None and user.pwd==password:
             session["username"] = username
             return redirect("index")
         else:
             message = "账号或密码错误，登录失败，请重新登录"
             return render_template('login.html', message=message)
    else:
        return render_template('login.html', message="请在此登录")
    return username


@app.route("/index")
@checkLogin
def index():
    print(Room.query.all())
    return render_template('rooms.html' , roomsInfo =Room.query.all())

#发起网络的都是str类型  要转为int类型
@app.route("/rooms/<roomid>")
@checkLogin
#查询房间信息
def getRoomsInfo(roomid):
    roomid= int(roomid)
    roomsInfo = Room.query.filter(Room.roomid == roomid).first() #取第一个
    now = datetime.datetime.now()
    # print(dir(datetime))
    ordersInfo = {}
    for i in range(1,11):
        delta = timedelta(days =i)
        n_days = now +delta
        ordersInfo[n_days.strftime('%Y-%m-%d')]="未预订"
    Orders = Order.query.filter(Order.roomid == roomid).all() #所有的数据查询集，返回对象列表
    # print(Orders)
    for ii in Orders:
        ordersInfo[ii.ordertime.strftime('%Y-%m-%d')] = "已预定"
    return render_template("roomsInfo.html",roomsInfo = roomsInfo,ordersInfo = ordersInfo)

#查询所有订单信息
@app.route("/order_all")
@checkLogin
def getordersInfo():
    return render_template("roomsInfo.html", ordersInfos=Order.query.all())


@app.route("/myinfo")
@checkLogin
def myinfo():
    username = session["username"]
    user_id = User.query.filter(User.username == username).first()
    user_id = user_id.userid
    print("my-----",user_id)
    #用户所预定的所有房间
    userrooms = Order.query.filter(Order.userid == user_id).all()
    roomslist = []
    price = []
    count_type = []
    for tmp in userrooms:
        roomstype = {}
        roomid = tmp.roomid
        type = Room.query.filter(Room.roomid==roomid).first()
        roomstype["userrooms"] = tmp.roomid
        roomstype["orderid"] = tmp.orderid
        roomstype["type"] = type.type
        count_type.append(type.type)
        roomstype["price"] = type.price
        ordertime = datetime.datetime.strftime(tmp.ordertime, '%Y-%m-%d')
        roomstype["ordertime"] = ordertime
        price.append(type.price)
        count_price = sum(price)
        roomslist.append(roomstype)
    print("这个是房间类型", count_type)
    count_rooms = {}
    for i in count_type:
        if count_rooms.get(i) == None:
            count_rooms[i] = 1
        else:
            count_rooms[i] = count_rooms[i] + 1
    print(count_rooms)
    roomslist.sort(key=itemgetter('ordertime'), reverse=True)
    print(roomslist)
    qu_ten=[]
    for ten in roomslist[:10]:
        qu_ten.append(ten)
    B = {"aa":11,"bb":22}
    return render_template("myinfo.html",username= username,roomslist =roomslist,count_price=count_price,count_rooms=count_rooms,qu_ten=qu_ten)

@app.route("/myinfo_ten")
@checkLogin
def myinfo_ten():
    username = session["username"]
    user_id = User.query.filter(User.username == username).first()
    user_id = user_id.userid
    print("my-----",user_id)
    #用户所预定的所有房间
    userrooms = Order.query.filter(Order.userid == user_id).all()
    #用户所预定的房间类型roomstype = {}
    roomslist = []
    price = []
    count_type = []
    for tmp in userrooms:
        roomstype = {}
        roomid = tmp.roomid
        type = Room.query.filter(Room.roomid==roomid).first()
        roomstype["userrooms"] = tmp.roomid
        roomstype["orderid"] = tmp.orderid
        roomstype["type"] = type.type
        count_type.append(type.type)
        roomstype["price"] = type.price
        ordertime = datetime.datetime.strftime(tmp.ordertime, '%Y-%m-%d')
        roomstype["ordertime"] = ordertime
        price.append(type.price)
        count_price = sum(price)
        roomslist.append(roomstype)
    print("这个是房间类型", count_type)
    #前10的房间类型
    count_rooms = {}
    for i in count_type:
        if count_rooms.get(i) == None:
            count_rooms[i] = 1
        else:
            count_rooms[i] = count_rooms[i] + 1
    print(count_rooms)
    roomslist.sort(key=itemgetter('ordertime'), reverse=True)
    print(roomslist)
    qu_ten=[]
    for ten in roomslist[:10]:
        qu_ten.append(ten)
    roomstype_ten=[]
    count_rooms = {}
    for i in qu_ten:
        count_rooms["type"]=type
        print('111',roomstype_ten)

        print("取10，，，，",i)

        # # 前10的房间类型
        # count_rooms = {}
        # for i in count_type:
        #     if count_rooms.get(i) == None:
        #         count_rooms[i] = 1
        #     else:
        #         count_rooms[i] = count_rooms[i] + 1
        # print(count_rooms)

    B = {"aa":11,"bb":22}
    return render_template("myinfo_ten.html",username= username,count_price=count_price,count_rooms=count_rooms,qu_ten=qu_ten)

@app.route("/bookroom/<roomid>/<booktime>")
@checkLogin
def bookroom(roomid,booktime):
    # print(login())
    roomid = int(roomid)
    booktime = datetime.datetime.strptime(booktime,'%Y-%m-%d')
    myorder = Order()
    myorder.roomid = roomid
    username = session["username"]
    user_id = User.query.filter(User.username == username).first()
    user_id = user_id.userid
    print("-----这个是userid",user_id)
    myorder.userid = user_id
    myorder.ordertime= booktime
    print('这个是myorder',myorder,'dddd')
    print('Order', Order, 'dddd')

    db.session.add(myorder)
    db.session.commit()
    bookroom_Info={}
    user = User.query.filter(User.userid == myorder.userid).first()
    ordertime = datetime.datetime.strftime(myorder.ordertime,'%Y-%m-%d')
    room = Room.query.filter(Room.roomid==myorder.roomid).first()
    Order_Info = Order.query.filter(Order.ordertime ==myorder.ordertime).first()
    bookroom_Info["username"]= user.username
    bookroom_Info["ordertime"]= ordertime
    bookroom_Info["roomid"]= myorder.roomid
    bookroom_Info["orderid"] = Order_Info.orderid
    bookroom_Info["type"] = room.type
    print(bookroom_Info)


    return render_template("bookroom.html",bookroom_Info=bookroom_Info)

@app.route("/logout",methods=("post","get"))
def logout():
    if request.method == 'GET':
        session.pop("username")
        return render_template("logout.html",message = "返回登录页面")


@app.route("/test")
def test():
    db.create_all()
    s1 = Student(name="zhangsan1")
    s2 = Student(name="lisi2")
    s3 = Student(name="wangwu3")
    s4 = Student(name="sunliu4")
    s5 = Student(name="zhangqi5")

    c1 = Course(name="Chinese",desc="this is chinese course")
    c2 = Course(name="English", desc="this is english course")
    c3 = Course(name="computer", desc="this is computer course")

    c1.students.append(s1)
    c1.students.append(s2)
    c1.students.append(s3)
    c1.students.append(s4)

    c2.students.append(s1)
    c2.students.append(s5)

    c3.students.append(s4)
    c3.students.append(s5)

    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)
    db.session.add(s4)
    db.session.add(s5)
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)

    db.session.commit()

    course = Course.query.filter(Course.name=="English").first()
    name = Student.query.filter(Student.name == "zhangsan1").all()
    print(name)
    print(name[0])
    print(name[0].courses)
    print(course.students)
    print(course.students[0].courses)
    return " "




if __name__ == '__main__':
    app.run()