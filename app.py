from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Kyven@123@121.4.38.213:3306/shumei?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
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

db.create_all()
#

@app.route("/index")
def index():
    return render_template('rooms.html' , roomsInfo =Room.query.all())

#发起网络的都是str类型  要转为int类型
@app.route("/rooms/<roomid>")
#查询房间信息
def getRoomsInfo(roomid):
    roomid= int(roomid)
    roomIofo = Room.query.filter(Room.roomid == roomid).all()
    now = datetime.now()
    orderInfo = {}
    for i in range(1,11):
        delta = timedelta(days =i)
        n_days = now +delta
        orderInfo[n_days.strftime('%Y-%m-%d')]="未预订"
        print(orderInfo)
    Orders = Order.query.filter(Order.roomid == roomid).all()
    for ii in Orders:
        print(ii)
        orderInfo[ii.ordertime.strftime('%Y-%m-%d')] = "已预定"
    # for tmp in Orders:
    #     orderInfo[tmp.orderTime.strftime('%Y-%m-%d')] = "被预订"
    #     orderInfo[tmp.orderTime.strftime('%Y-%m-%d')] = "被预订"
    # # orderInfo = Order.query.filter(Order.roomid == roomid)
    # # print(orderInfo)
    return render_template("roomsInfo.html",roomIofo = roomIofo,orderInfo = orderInfo)

#查询所有订单信息
@app.route("/order_all")
def getorderInfo():
    return render_template("roomsInfo.html", orderInfo=Order.query.all())

@app.route("/bookroom")
def bookroom():
    return render_template("bookroom.html")

