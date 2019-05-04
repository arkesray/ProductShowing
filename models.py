from ProductShowing import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Products(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    img=db.Column(db.String(250))
    code=db.Column(db.String(50), unique=True)
    color=db.Column(db.String(50))
    warrenty=db.Column(db.String(50))
    price=db.Column(db.String(50))
    mfg=db.Column(db.String(50))
    exp=db.Column(db.String(50))
    description=db.Column(db.String(100))

    def __init__(self,name,img,code,color,war,price,mfg,exp,d):
        self.name=name
        self.img=img
        self.code=code
        self.color=color
        self.warrenty=war
        self.price=price
        self.mfg=mfg
        self.exp=exp
        self.description=d



