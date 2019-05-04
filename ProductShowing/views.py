import os
import datetime
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from flask import render_template, session, redirect, request, url_for, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from ProductShowing import app
from models import db, Products
EMAIL_='arkesray@gmail.com'
PASS_='***********'
Session(app)

db.create_all()
path = os.path.abspath('') + "\\ProductShowing\\static\\img\\"
print(path)
# manually adding products to database
x = []
x.append(Products('car','car.jpg','CAR-01','red','5 years','5 Lakhs','2019','None','A very good long lasting car.'))
x.append(Products('pen','pen.jpg','PEN-01','red-black','1 years','10 Rs','2018','3 months','Super smooth pen.'))
x.append(Products('fan','fan.jpg','FAN-01','blue','3 years','1 thousand','2019','None', 'Gusting with Power'))
x.append(Products('ledbulb','ledbulb.jpg','LED-01','white','2 years','500 Rs','2018','5 years', 'Bright glow'))
x.append(Products('camera','camera.jpg','CAM-01','black','10 years','1 Lakhs','2019','None', 'Quality Photos'))
x.append(Products('mobile','mobile.jpg','CELL-01','black','1 years','5 thousand','2019','None', 'Communication deveice'))
x.append(Products('torch','torch.jpg','LED-02','black-yellow','1 years','100 Rs','2019','None', 'Remove darkness'))

for i in range(7):
    try:
        db.session.add(x[i])
        db.session.commit()
    except:
        print("Error adding to database")
        db.session.rollback()
        pass

#routes
@app.route('/')
@app.route('/products', methods=["GET","POST"])
def products():
    if request.method == "GET":
        p = Products.query.all()
        search = request.args.get('search')
        if search == None:
            return render_template('products.html', resmsg = "Showing all Products", title = 'Products', products = p)
        #print(p, search)
        prd = []
        """
        for item in p:
            if search.lower() == item.name.lower():
                prd.append(item)

        """
        #my own search engine (advanced)
        
        wordCntList = []
        d1 = {}
        words = search.strip().split()
        #print(words)
        for word in words:
            for c in 'abcdefghijklmnopqrstuvwxyz':
                d1[c] = word.lower().count(c)
            wordCntList.append((d1.copy(),len(word))) 

        for item in p:
            for c in 'abcdefghijklmnopqrstuvwxyz':
                d1[c] = item.name.lower().count(c) 
            for e in wordCntList:
                cnt = 0
                for k,v in e[0].items():
                    if (v>0) and (abs(v - d1[k]) > 0.5):
                        cnt += 1
                #print(cnt, e[1]/2 - .5)
                if cnt < e[1]/2 - 0.5 :
                    if item not in prd:
                        prd.append(item)

        return render_template('products.html', resmsg = str(len(prd)) + " results found for '" + search +"'", fill = search, title = 'Products', products = prd)
    else:
        
        productId = request.form.get('prdId')
        email = request.form.get('email')
        #print(email,productId)
        p = Products.query.filter_by(id=productId).first()

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(EMAIL_, PASS_)
        msg = MIMEMultipart('related')
        msg['From']=EMAIL_
        msg['To']=email
        msg['Subject']="We think You are interested in our Product"

        message = "This is a msg generated from ProductShowing Website\n Your currently choiced Product Details :- "
        message += "\n Name : " + p.name + "\n Code : " + p.code + "\n Color : " + p.color + "\n Price : " + p.price + "\n Warrenty : " + p.warrenty + "\n Description : " + p.description
        msg.attach(MIMEText(message, 'plain'))
        image = MIMEImage(open(path+p.img, 'rb').read())
        msg.attach(image)
        
        s.send_message(msg)
        del msg
        s.quit()
        
        return render_template('products.html', sent=1, resmsg = "Confirmation", title = 'Products', products=[p])

