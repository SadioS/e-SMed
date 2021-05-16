# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 11:03:38 2021

@author: sadio_aya5cf2
"""
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def create_db():
    if 'db' not in g:
        g.db= sqlite3.connect('mydatabase.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def addUser(nom, prenom, date, mail, mdp):
    with sqlite3.connect("mydatabase.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO clients(nom, prenom, date, mail, mdp) VALUES(?,?,?,?,?)" , (nom, prenom, date, mail, mdp))
        con.commit()
    con.close()
    
def verifUser(mail, mdp): 
    with sqlite3.connect("mydatabase.db") as con:
        cur = con.cursor()
        cur.execute("SELECT mdp FROM clients WHERE mail=?" , (mail,))
        reponse = cur.fetchone()
        con.commit()
    con.close()
    if reponse == mail:
        return('/valide.html')
    
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)    
    
conn = sqlite3.connect('mydatabase.db')
print('Base de données ouverte avec succès')
conn.execute ('CREATE TABLE clients (nom TEXT, prenom TEXT, date VARCHAR, mail TEXT, mdp VARCHAR)')
print('Table crée avec succès')
conn.close()