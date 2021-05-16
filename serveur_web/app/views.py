# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 23:50:10 2021

@author: sadio_aya5cf2
"""
from app import app
from flask import Flask, session, render_template, request, g, current_app, redirect, url_for
import sqlite3
import click
from flask import current_app, g
import random
import hashlib, uuid, os
import datetime

###### entré dans la base de donnée ######
def get_db():
    if 'db' not in g:
        g.db= sqlite3.connect('mydatabase.db')
        g.db.row_factory = sqlite3.Row
    return g.db


###### page d'accueil ######
@app.route('/')
def accueil():
    return render_template ('home.html')
    #db.execute("INSERT INTO donneep(nom, prenom, d, mail, num, date, adresse) VALUES(?,?,?,?,?,?,?)" , (nom, prenom, mdp, mail, num, date, adresse))
    # db.commit()
    
################################################ Nouvel utilisateur #######################################

###### création d'un nouvel espace utilisateur ######
@app.route('/new', methods=('GET', 'POST'))
def new():
    #if request.method == 'POST':
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    date = request.form.get('date')
    mail = request.form.get ('mail')
    tel = request.form.get('num')
    mdp = request.form.get('mdp')
    mdp_hash = hashlib.sha256(str(mdp).encode("utf-8")).hexdigest()
    adresse = request.form.get('adresse')
    code = request.form.get('poste')
    ville = request.form.get('ville')
    
    db = get_db()
    
    #création id patient unique
    a= random.randint(0,9)
    b= random.randint(0,9)
    c= random.randint(0,9)
    d= random.randint(0,9)
    e= random.randint(0,9)
    
    idp = 'p' + str(a) + str(b)+str(c) + str(d) +str(e)
    
    """verifier si l'e-mail n'est pas deja utilise par un client"""

    patient_existant = db.execute("SELECT * FROM donneep WHERE mail =? ", (mail,)).fetchall()
    print(len(patient_existant))
    id_existant = db.execute("SELECT * FROM donneep WHERE id =? ", (idp,)).fetchall()
    print(len(id_existant))
    
    '''Si on a déjà un e-mail avec cette adresse, on dit que le mail est déjà utilisé'''

    if len(patient_existant) > 0:
        error = 'Cette adresse courriel est deja utilisée, veuillez utiliser une autre adresse.'
        return render_template("new2.html", error = error)
    #"""Sinon on enregistre les informations du client dans la BD"""

    else:
        if len(id_existant) > 0:
            a= random.randint(0,9)
            b= random.randint(0,9)
            c= random.randint(0,9)
            d= random.randint(0,9)
            e= random.randint(0,9)
            idp = 'p' + str(a) + str(b)+str(c) + str(d) +str(e)
        else:
            db.execute("INSERT INTO donneep(nom, prenom, date_n, mail, tel, adresse, code, ville, mdp, id) VALUES(?,?,?,?,?,?, ?, ?, ?,?)" , (nom, prenom, date, mail, tel, adresse, code, ville, mdp_hash, idp))
    # db.execute("INSERT INTO tests(mail, hématie, hémogobline, hématocrite, VGM, TCMH, CCMH, Leucocytes, PE, PN, PB, lymphocytes, monocytes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",  (mail, Hématie, Hémoglobine, Hématocrite, VGM, TCMH, CCMH, Leucocytes, PE, PN, PB, Lymphocytes, Monocytes))
    #db.execute("INSERT INTO resultats(nom, prenom, mdp, mail, num, date, adresse) VALUES(?,?,?,?,?,?,?)" , (nom, prenom, mdp, mail, tel, date, adresse))
   
    db.execute('INSERT INTO patients(nom, mdp, mail, num, date) VALUES (?,?,?,?,?)', (nom, mdp_hash, mail, tel, date))
    test = db.execute("SELECT id FROM donneep WHERE mail=?", (mail,)).fetchall()
    db.commit()
    if len(test) == 1:
            return render_template('info.html', idp=idp)
    return render_template('new2.html')   


####################### Renseignement id patient #############################
@app.route('/info', methods=('GET', 'POST'))
def info():
    return render_template('info.html')

    
############################################# PARTIE PATIENT ######################################  

###### accés à son espace personnel ######
#patients / médecins / créer son espace
@app.route('/espace_personnel')
def eperso():
    return render_template ('eperso.html')


###### connexion espace patient ######
@app.route('/login', methods=('GET', 'POST'))
def login():
    print('login()')
    #if request.method == 'POST':
    idp = request.form.get('idp')
    mdp = request.form.get('mdp')
    mdp_t = hashlib.sha256(str(mdp).encode("utf-8")).hexdigest()
   
    con = sqlite3.connect("mydatabase.db") 
    #con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute("SELECT mdp FROM donneep WHERE id=?", (idp,)) 
    user = user.fetchall()
            
    prenom = cur.execute("SELECT prenom FROM donneep WHERE id=?", (idp,))
    for row in prenom:
        for d in row:
            user1 = d
            print(user1)
 
    if len(user) == 1:
        return render_template('tbord.html', idp=idp, prenom=user1)
    return render_template('login.html')

##### accès tableau de bord patient ######
@app.route('/tbord')
def tbord():
    return render_template ('tbord.html')

######## espace rendez-vous ########
@app.route('/e_rdv')
def e_rdv():
    idp = request.form.get('idp')
    return render_template('choix_rdv.html', idp=idp)


###### prise de rendez-vous patient ######
@app.route('/rdv', methods=('GET', 'POST'))
def rdv():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    date = request.form.get('date')
    idp = request.form.get('idp')
    heure = request.form.get('heure')
    medecin = request.form.get('spe')
    message = request.form.get('message')
    num= random.randint(0, 1000)
    
    L=[1, 2, 3]
    print('rdv_test =', idp)
    db = get_db()
    
    idm = db.execute("SELECT idm FROM donneem WHERE specialite=?", (medecin,))
  # idm1 = idm.fetchall()[0][0]
    for row in idm:
        for d in row:
            idm1 = d
            del L[0]
            L.append(idm1)
            print(L, idm1)
  
    idm = db.execute("SELECT salle FROM donneem WHERE specialite=?", (medecin,))
    #salle = idm.fetchall()[0][1]
    for row in idm:
        for d in row:
            salle = d
            del L[0]
            L.append(salle)
            print(L, salle)
            
    name = db.execute("SELECT nom FROM donneem WHERE specialite=?", (medecin,))
    #salle = idm.fetchall()[0][1]
    for row in name:
        for d in row:
            name = d
            del L[0]
            L.append(name)
            print(L, name)
    
    db.execute('INSERT INTO inter(date, idp, heure, med, num, idm, dr) VALUES (?,?,?,?,?,?,?)', (date, idp, heure, medecin, num, L[0], L[2]))
    db.commit()
    test = db.execute("SELECT idp FROM inter WHERE date=? and heure=?", (date, heure)).fetchall()
    print(L)
    db.execute("DELETE FROM inter WHERE idp = ''")
   
    if len(test) == 1:
            print('rdv_test =',idp)
            #return redirect(url_for('rdv_ok'), liste = liste) 
            return render_template ('Ok.html', idp=idp, nom=nom, prenom=prenom, date=date, heure=heure, medecin=medecin, num=num, idm1=idm1, salle=salle, name=name)
    return render_template ('rdv.html', idp=idp)
    
@app.route('/rdv_ok', methods=('GET', 'POST'))
def rdv_ok():
    
   
    db = get_db()
 
    idp = request.form.get('idp')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    date = request.form.get('date')
    num = request.form.get('num')
    heure = request.form.get('heure')
    medecin = request.form.get('spe')
    idm1 = request.form.get('idm1')
    salle= request.form.get('salle')
    db.execute("DELETE FROM inter WHERE idp = NULL")
        
   #  rdv = db.execute("SELECT date FROM inter WHERE idp=?", (idp,))
   #  print("tuple=", rdv)
   #  #date = rdv.fetchall()[0][0]
   #  for row in rdv:
   #      for d in row:
   #          date = d
   #          print("date=", date)
            
   
   #  rdv = db.execute("SELECT  heure FROM inter WHERE idp=?", (idp,))
   #  for row in rdv:
   #      for d in row:
   #          heure = d
   #          print("heure = ", heure)
   #  #heure = rdv.fetchall()[0][1]
    
   #  rdv = db.execute("SELECT med FROM inter WHERE idp=?", (idp,))
   #  #medecin = rdv.fetchall()[0][2]
   #  for row in rdv:
   #      for d in row:
   #          medecin = d
   #          print("med=", medecin)
    
   #  rdv = db.execute("SELECT  num FROM inter WHERE idp=?", (idp,))
   # # num = rdv.fetchall()[0][3]
   #  for row in rdv:
   #      for d in row:
   #          num = d
   #          print("num=", num)
    
    
    
    # print('idm1 =', idm1)
    # print('salle =', salle)
    #print(type(idm1))
   
    # for row in idm1:
    #     for d in row:
    # #         idm2 = d
    #         print('d=' , d)        
   
    
    # salle = db.execute("SELECT salle FROM donneem WHERE specialite=?", (medecin,))
    # salle = salle.fetchall()
    # for row in salle:
    #     for d in row:
    #         salle1 = d
    #         print('salle1=', salle1)
   
    #db.execute("INSERT INTO tests(mail, hématie, hémogobline, hématocrite, VGM, TCMH, CCMH, Leucocytes, PE, PN, PB, lymphocytes, monocytes) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",  (mail, Hématie, Hémoglobine, Hématocrite, VGM, TCMH, CCMH, Leucocytes, PE, PN, PB, Lymphocytes, Monocytes))
    
    if idm1 !=0 or salle !=0 or idp!=0 or date!=0 or heure!=0:
        db.execute("INSERT INTO rdv(idp, idm, date, heure, salle, num) VALUES(?,?,?,?,?,?)" , (idp, idm1, date, heure, salle, num))
        db.commit()
    test = db.execute("SELECT num FROM rdv WHERE idp=?", (idp,)).fetchall()
    print('idp =', idp)
    if len(test) == 1:
            return render_template('login.html', idp=idp, test=test)#, idm1, idp, date, heure, salle)
    return render_template ('Ok.html', idp=idp)

# @app.route('/verif', methods=('GET', 'POST'))
# def vérif():
#     idp = request.form.get('idp')
#     nom = request.form.get('nom')
#     con = sqlite3.connect("mydatabase.db") 
#     #con.row_factory = sqlite3.Row
#     cur = con.cursor()
#     user = cur.execute("SELECT mdp FROM donneep WHERE id=?", (idp,)) 
#     user = user.fetchall()
#     if len(user) == 1:
#             #return redirect(url_for('rdv_ok'), liste = liste) 
#             return render_template ('recap.html', idp=idp)
#     return render_template ('verif.html')

@app.route("/verif", methods=["GET", "POST"])
def verif():
    idp = request.form.get('idp')
    con = sqlite3.connect("mydatabase.db") 
    #con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    pat = cur.execute("SELECT * FROM inter WHERE idp =? ", (idp,))
    pat = pat.fetchall()
    print(pat)
    
    med = cur.execute("SELECT idm FROM inter WHERE idp =? ", (idp,))
    med = med.fetchall()
    print(med)
    
    
    med1 = cur.execute("SELECT nom FROM donneem WHERE idm =? ", (idp,))
    med1 = med1.fetchall()
    print(med1)
    
    nom = cur.execute("SELECT nom, prenom FROM donneep WHERE id=? ", (idp,))
    nom = nom.fetchall()
    print(med1)
    
    
    # D=[]
    # date = cur.execute("SELECT date FROM inter WHERE idp =? ", (idp,))
    # date = date.fetchall()
    # for row in date:
    #     for d in row:
    #         date = d
    #         D.append(date)
    # print(date, D)
    
    rdv=[]
    
    # for d in D:
    #     if d < str(datetime.date.today()):
    #         pat = cur.execute("SELECT * FROM inter WHERE idp =? ", (idp,))
    #         pat = pat.fetchall()
    #         rdv.append(pat)
    #         print(rdv ,'=rdv')
            
    
    # user = cur.execute("SELECT * FROM vaccin WHERE id =? ", (idp,))
    # vac = user.fetchall()
    # print(vac)
    # user1 = cur.execute("SELECT * FROM vaccin_rec WHERE id =? ", (idp,))
    # vac1 = user1.fetchall()
    # print(vac1)
    # user2 = cur.execute("SELECT * FROM med WHERE id =? ", (idp,))
    # MED = user2.fetchall()
    # print(MED)
    # chemin= "app/fhir/patients/"+str(pat)+".py"
    
    # if pat == 'pat1':
    #   return render_template('pat1.html') 
    # if pat == 'pat2':
    #   return render_template('pat2.html')
    # if pat == 'pat3':
    #   return render_template('pat3.html')
        # fichier = open(chemin, 'r') 
        # nom = fichier.json_dict.name[0] 
        # prenom = fichier.json_dict.name[1] 
        # date = fichier.json_dict.birthDate
        # iid = fichier.json_dict.id
        # vac1 = fichier.vac1.vaccinCode[1]
        # vac2 = fichier.vac2.recommendation[0][0][2]
        # return render_template("index.html", nom = nom, prenom=prenom, date=date, vac1=vac1, vac2=vac2, iid=iid)
        
    if len(nom) != 0: # or len(vac1) == 1 or len(MED) == 1:
        return render_template("recap.html", pat=pat, med1=med1, nom=nom)#, vac=vac, vac1=vac1, MED=MED)
    
    return render_template("verif.html")

@app.route('/recap', methods=('GET', 'POST'))
def recap():
    db = get_db()
    #idp = "p60954"
   # idp = request.form['idpt']
    #print("idp=", idp)
    idp='p17394'
    
    con = sqlite3.connect("mydatabase.db") 
    #con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute("SELECT * FROM inter WHERE idp =? ", (idp,))
    rdv = user.fetchall()
    
    
    # rdv = db.execute("SELECT * FROM inter WHERE idp =? ", (idp,))
    # rdv = rdv.fetchall
    print("RDV=", rdv)
    print(idp)
    return render_template ('recap.html', rdv=rdv, idp=idp)

@app.route('/doc_p', methods=('GET', 'POST'))
def doc_p():
    return render_template('doc_p.html')

########################### Visualiser ses documents ##########################
@app.route('/choix')
def choix():
    #permet de choisir l'affichage souhaité de nos résultats
    return render_template ('choix2.html')

@app.route("/verif_t", methods=["GET", "POST"])
def verif_t():
    idp = request.form.get('idp')
    mdp = request.form.get('mdp')
    con = sqlite3.connect("mydatabase.db") 
    #con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    user = cur.execute("SELECT mdp FROM donneep WHERE id=?", (idp,)) 
    user = user.fetchall()
    
    pat = cur.execute("SELECT * FROM tests WHERE id =? ", (idp,))
    pat = pat.fetchall()
    print(pat)
    
    med = cur.execute("SELECT * FROM med WHERE id =? ", (idp,))
    med = med.fetchall()
    print(med)
    
    # med = cur.execute("SELECT idm FROM inter WHERE idp =? ", (idp,))
    # med = med.fetchall()
    # print(med)
    
    
    # med1 = cur.execute("SELECT nom FROM donneem WHERE idm =? ", (idp,))
    # med1 = med1.fetchall()
    # print(med1)
    
    nom = cur.execute("SELECT nom, prenom FROM donneep WHERE id=? ", (idp,))
    nom = nom.fetchall()
    print(nom)
    
    if len(user) ==0:
        error = 'Mauvais identifiant ou mot de passe, veuillez réessayer! '
        return render_template("verif.html", error = error)
    if len(pat) != 0: # or len(vac1) == 1 or len(MED) == 1:
        return render_template("test.html", pat=pat, nom=nom, med=med)#, vac=vac, vac1=vac1, MED=MED)
    return render_template("verif.html")

@app.route("/verif_p", methods=["GET", "POST"])
def verif_p():
    
    idp = request.form.get('idp')
    mdp = request.form.get('mdp')
    con = sqlite3.connect("mydatabase.db") 
    #con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    user = cur.execute("SELECT mdp FROM donneep WHERE id=?", (idp,)) 
    user = user.fetchall()
    
    pat = cur.execute("SELECT * FROM tests WHERE id =? ", (idp,))
    pat = pat.fetchall()
    print(pat)
    
    med = cur.execute("SELECT * FROM med WHERE id =? ", (idp,))
    med = med.fetchall()
    print(med)
    
    # med = cur.execute("SELECT idm FROM inter WHERE idp =? ", (idp,))
    # med = med.fetchall()
    # print(med)
    
    
    # med1 = cur.execute("SELECT nom FROM donneem WHERE idm =? ", (idp,))
    # med1 = med1.fetchall()
    # print(med1)
    
    nom = cur.execute("SELECT nom, prenom FROM donneep WHERE id=? ", (idp,))
    nom = nom.fetchall()
    print(nom)
    
    if len(user) ==0:
        error = 'Mauvais identifiant ou mot de passe, veuillez réessayer! '
        return render_template("verif.html", error = error)
    if len(user) != 0: # or len(vac1) == 1 or len(MED) == 1:
        return render_template("pdf.html", pat=pat, nom=nom, med=med)#, vac=vac, vac1=vac1, MED=MED)
    return render_template("verif.html")

@app.route('/sup', methods=('GET', 'POST'))
def sup():
    num = request.form.get('num')
    
    con = sqlite3.connect("mydatabase.db") 
    cur = con.cursor()
    
    pat = cur.execute("DELETE FROM inter WHERE num =? ", (num,))
    pat = pat.fetchall()
    
    user = cur.execute("SELECT * FROM inter WHERE num =? ", (num,))
    user = user.fetchall()
    
    if len(user) > 0:
        return render_template('sup.html')
   
    return render_template('sup.html')
    
###################################### PARTIE MEDECIN ####################################"
@app.route('/tbord_m', methods=('GET', 'POST'))
def tbord_m():
    return render_template('tbord-m.html')

###### Accès espace personnel médecin ######
@app.route('/loginm', methods=('GET', 'POST'))
def loginm():
    #if request.method == 'POST':
    idm = request.form.get('idm')
    mdp = request.form.get('mdp')
   
    con = sqlite3.connect("mydatabase.db") 
    #con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute("SELECT idm FROM donneem WHERE idm=?", (idm,))    
    user = user.fetchall()
    print(user)
    if len(user) ==0:
        error = 'Mauvais identifiant ou mot de passe, veuillez réessayer! '
        return render_template("loginm.html", error = error)
    if len(user) == 1:
        return render_template('tbord-m.html')
    return render_template('loginm.html')


###### Accès donnée patient ######
@app.route("/fhir", methods=["GET", "POST"])
def fhir():
    idp = request.form.get('nom')
    con = sqlite3.connect("mydatabase.db") 
    #con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    pat = cur.execute("SELECT * FROM donneep WHERE id =? ", (idp,))
    pat = pat.fetchall()
    print(pat)
    
    user = cur.execute("SELECT * FROM vaccin WHERE id =? ", (idp,))
    vac = user.fetchall()
    print(vac)
    user1 = cur.execute("SELECT * FROM vaccin_rec WHERE id =? ", (idp,))
    vac1 = user1.fetchall()
    print(vac1)
    user2 = cur.execute("SELECT * FROM med WHERE id =? ", (idp,))
    MED = user2.fetchall()
    print(MED)
    # chemin= "app/fhir/patients/"+str(pat)+".py"
    
    # if pat == 'pat1':
    #   return render_template('pat1.html') 
    # if pat == 'pat2':
    #   return render_template('pat2.html')
    # if pat == 'pat3':
    #   return render_template('pat3.html')
        # fichier = open(chemin, 'r') 
        # nom = fichier.json_dict.name[0] 
        # prenom = fichier.json_dict.name[1] 
        # date = fichier.json_dict.birthDate
        # iid = fichier.json_dict.id
        # vac1 = fichier.vac1.vaccinCode[1]
        # vac2 = fichier.vac2.recommendation[0][0][2]
        # return render_template("index.html", nom = nom, prenom=prenom, date=date, vac1=vac1, vac2=vac2, iid=iid)
    if len(pat)==0 and len(vac) == 0 and len(vac1) == 0 and len(MED) == 0:
        error = "Ce patient n'existe pas. Nous n'avons aucune donnée le concernant"
        return render_template("index2.html", error=error)
        
    if len(pat)==1 or len(vac) == 1 or len(vac1) == 1 or len(MED) == 1:
        return render_template("resultat.html", pat=pat, vac=vac, vac1=vac1, MED=MED)
    
    return render_template("index2.html")

@app.route("/verif_m", methods=["GET", "POST"])
def verif_m():
    idm = request.form.get('idm')
    con = sqlite3.connect("mydatabase.db") 
    #con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    pat = cur.execute("SELECT * FROM inter WHERE idm =? ", (idm,))
    pat = pat.fetchall()
    print(pat)
    
    # med = cur.execute("SELECT idm FROM inter WHERE idp =? ", (idp,))
    # med = med.fetchall()
    # print(med)
    
    
    # med1 = cur.execute("SELECT nom FROM donneem WHERE idm =? ", (idp,))
    # med1 = med1.fetchall()
    # print(med1)
    
    # nom = cur.execute("SELECT nom, prenom FROM donneep WHERE id=? ", (idp,))
    # nom = nom.fetchall()
    # print(med1)
    
    
    # D=[]
    # date = cur.execute("SELECT date FROM inter WHERE idp =? ", (idp,))
    # date = date.fetchall()
    # for row in date:
    #     for d in row:
    #         date = d
    #         D.append(date)
    # print(date, D)
    
    rdv=[]
    
    # for d in D:
    #     if d < str(datetime.date.today()):
    #         pat = cur.execute("SELECT * FROM inter WHERE idp =? ", (idp,))
    #         pat = pat.fetchall()
    #         rdv.append(pat)
    #         print(rdv ,'=rdv')
            
    
    # user = cur.execute("SELECT * FROM vaccin WHERE id =? ", (idp,))
    # vac = user.fetchall()
    # print(vac)
    # user1 = cur.execute("SELECT * FROM vaccin_rec WHERE id =? ", (idp,))
    # vac1 = user1.fetchall()
    # print(vac1)
    # user2 = cur.execute("SELECT * FROM med WHERE id =? ", (idp,))
    # MED = user2.fetchall()
    # print(MED)
    # chemin= "app/fhir/patients/"+str(pat)+".py"
    
    # if pat == 'pat1':
    #   return render_template('pat1.html') 
    # if pat == 'pat2':
    #   return render_template('pat2.html')
    # if pat == 'pat3':
    #   return render_template('pat3.html')
        # fichier = open(chemin, 'r') 
        # nom = fichier.json_dict.name[0] 
        # prenom = fichier.json_dict.name[1] 
        # date = fichier.json_dict.birthDate
        # iid = fichier.json_dict.id
        # vac1 = fichier.vac1.vaccinCode[1]
        # vac2 = fichier.vac2.recommendation[0][0][2]
        # return render_template("index.html", nom = nom, prenom=prenom, date=date, vac1=vac1, vac2=vac2, iid=iid)
        
    if len(pat) != 0: # or len(vac1) == 1 or len(MED) == 1:
        return render_template("recap_m.html", pat=pat)#, vac=vac, vac1=vac1, MED=MED)
    
    return render_template("rdv_m.html")

@app.route("/fhir_modif", methods=["GET", "POST"] )

 
#####################################################################################################




@app.route('/valide')
def valide():
    #résutat affiché
    return render_template ('index2.html')
@app.route('/pdf')
def pdf():
    return render_template ('pdf.html')
