# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 22:05:23 2021

@author: sadio_aya5cf2
"""
import sqlite3
from flask import request

def but(mail, mdp):
    mdp = request.form.get('mdp')
    mail = request.form.get('mail')
    with sqlite3.connect("mydatabase.db") as con:
       con.row_factory = sqlite3.Row
       cur = con.cursor()
       user = cur.execute("SELECT mdp FROM patients WHERE mail=?" , (mail,)).fetchall()[0]
       con.commit()
    con.close()
    return user
   