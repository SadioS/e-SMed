# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 13:27:17 2021

@author: sadio_aya5cf2
"""

import sqlite3
import click
from flask import current_app, g
import random

def get_db():
    if 'db' not in g:
        g.db= sqlite3.connect('mydatabase.db')
        g.db.row_factory = sqlite3.Row
    return g.db

 #création id patient unique
a= random.randint(0,9)
b= random.randint(0,9)
c= random.randint(0,9)
d= random.randint(0,9)
e= random.randint(0,9)

id = 'p' + str(a) + str(b)+str(c) + str(d) +str(e)

nom= input("nom: ")
prenom= input("prenom: ")
date= input("date: ")
mail=input("mail: ")
tel= input("tel: ")
adresse= input("ad: ")
code= input("code: ")
ville= input("ville: ")
mdp= input("mdp: ")


# db.execute("INSERT INTO tests(mail, hématie, hémogobline, hématocrite, VGM, TCMH, CCMH, Leucocytes, PE, PN, PB, lymphocytes, monocytes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",  (mail, Hématie, Hémoglobine, Hématocrite, VGM, TCMH, CCMH, Leucocytes, PE, PN, PB, Lymphocytes, Monocytes))
db = get_db()
db.execute("INSERT INTO donneep(nom, prenom, daten, mail, tel, adresse, code, ville, mdp, id) VALUES(?,?,?,?,?,?,?, ?, ?, ?)" , (nom, prenom, date, mail, tel, adresse, code, ville, mdp, id))
db.commit()