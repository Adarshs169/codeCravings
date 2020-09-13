# -*- coding: utf-8 -*-
"""
@author: adars
"""
import pyqrcode
import hashlib
import png
import sqlite3
#Database connected
#con=sqlite3.connect('data.db')
    #Function to create table if not created and insert the values
def addtodb(codeval,encryptedcode):
       #con=sqlite3.connect('data.db')
       try:
        con=sqlite3.connect('data.db')
        con.execute('create table codetab (code varchar(40) , encodedhash varchar(100));')
       except:
        pass
       con=sqlite3.connect('data.db')
       cur=con.cursor()
       try:
        cur.execute('insert into codetab (code,encodedhash) values(?,?);',(codeval, encryptedcode))
        con.commit()
        cur.close()
        con.close()
       except:
        print('Alert Alert')
#Function to generate QR code
def codegenerator(code):
       #Given code is SHA256 Encrypted before generating the QR
       encodedcode=hashlib.sha256(code.encode())
       qrcode=pyqrcode.create(str(encodedcode.hexdigest()))
       qrcode.png('/static/uca-colors.png', scale=6,module_color=[0, 0, 0, 128])
       # the code and its corresponding hash value is added to database
       print(str(encodedcode.hexdigest()))
       addtodb(code,str(encodedcode.hexdigest()))
    # Function to Read the QR code takes image name as input,uses opencv
#Flask to create an api
from flask import Flask, render_template
app=Flask(__name__)
@app.route('/')
def index():
     return render_template('index.html')

@app.route('/code/<qrcodeval>')
def outputgenerator(qrcodeval):
            #Checks if the scanned code exists in database
       con=sqlite3.connect('data.db')
       cursor=con.cursor()
       try:
        cursor.execute('select code from codetab where encodedhash=?',(qrcodeval,))
       except:
        print("Errrrrrrrror")
       record=cursor.fetchone()
       if record!=None:
            return "True"
       else:
            return "False"
code=input('Enter the Company Code:')
code=code+input('Enter the Medicine Code:')
code=code+input('Enter the strip code:')
#QR Code created:
codegenerator(code)
app.run()



