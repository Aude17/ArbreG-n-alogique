import sqlite3
# on a besoin de cette bibliothèque pour manipuler sql
# on creer la fonction qui va elle meme creer deux table la premiere qui est la table des element de l arbre
def creer_tables():
    conn = sqlite3.connect('arbre.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Personne")
    cur.execute("""CREATE TABLE Personne (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname TEXT,
    lname TEXT,
    address TEXT,
    phone TEXT,
    birthday DATE,
    fathername TEXT,
    fatherbirthday DATE,
    motherfirstname TEXT,
    motherlastname TEXT,
    motherbirthday DATE,
    idfather INT,
    idmother INT)""")

    conn.close()
    #on creer une table dedier au nom d utilisateur et de mot de passe
    conn = sqlite3.connect('arbre.db')
    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS Identite""")
    cur.execute("""CREATE TABLE Identite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    admin INT)""")

    conn.close()

# la fonction en parametre le nom d une des table et un tuple (un ensenble de variable comme un tableau)
# la fonction verifie uniquement si le nom de la table est bien saisi et que la taille du tuple correspond à la table
# mais attention a l ordre des variable
# le tuple peut avoir plusieur variable a null
def insertion(table, tuple):
    if table == 'Identite':
        if len(tuple)!=3:
            return False
        else:
            conn = sqlite3.connect('arbre.db')
            cur = conn.cursor()
            cur.execute("""INSERT INTO Identite (username, password)
                VALUES (?, ?, ?)""", tuple)
            conn.commit()
            conn.close()
            return  True

    elif table == 'Personne':
        if len(tuple)!= 12:
            return False
        else:
            conn = sqlite3.connect('arbre.db')
            cur = conn.cursor()
            cur.execute("""INSERT INTO Personne (fname, lname, address, phone, birthday, fathername, fatherbirthday, motherfirstname, motherlastname, motherbirthday, idfather, idmother)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,)""", tuple)
            conn.commit()
            conn.close()
            return True
    else:
        return False


# la fonction modification prend en paramètre la table de la cible, les nouvelles information dans quel catégorie et
# enfin id de la cible
def modification(table, tuple, category, idtarget):
    if table == 'Personne' or table == 'Identite':
        if len(tuple) == len(category):
            conn = sqlite3.connect('arbre.db')
            cur = conn.cursor()
            for i in range(len(tuple)):
                a = tuple[i]
                b = category[i]
                sql = f"UPDATE {table} SET {b} = ? WHERE id = ?"
                cur.execute(sql, (a, idtarget))
                conn.commit()
            conn.close()
            return True
    else:
        return False

def noeud_suppression(table, idtarget):
    if table == 'Personne' or table == 'Identite':
        conn = sqlite3.connect('arbre.db')
        cur = conn.cursor()
        cur.execute(f"""DELETE FROM {table}
            WHERE id = ?""", (idtarget,))
        conn.commit()
        conn.close()

        conn = sqlite3.connect('arbre.db')
        cur = conn.cursor()
        cur.execute(f"""SELECT id FROM {table}
                          WHERE (idmother = ? OR idfather = ?) AND (idmother IS NULL OR idfather IS NULL)""", (idtarget, idtarget))
        res = cur.fetchall()
        conn.close()
        for i in res:
            noeud_suppression(table, i)
        return True
    return False

def size_tree():
    res = 0
    conn = sqlite3.connect('arbre.db')
    cur = conn.cursor()
    res = cur.execute("""SELECT count() FROM Personne""")
    print(res.fetchone())
    conn.close()

def suppression_compte():
    takeuser = 0
    takepass = 0

# rajouter la saisi au clavier avec variable saisis et verifpass pour enregistrer les valeurs saisi.
    conn = sqlite3.connect('arbre.db')
    cur = conn.cursor()
    res = cur.execute("""DELETE FROM Identite
                      where username = ? OR password = ?""", (takeuser,), (takepass,))
    conn.close()


def show(tables, idtarget):
    return False

# rajouter la saisi au clavier avec variable saisis et verifpass pour enregistrer les valeurs saisi.
def connexion():
    saisi = 0
    verifname = 0
    verifpass = 0
    conn = sqlite3.connect('arbre.db')
    cur = conn.cursor()
    verifname = cur.execute(f"""SELECT * FROM Identite
                            WHERE username = {saisi}""")
    if (saisi != verifname[0] or verifpass != verifname[1]):
        return False
    return True

def insertion_Personne():
    takebirtfday = 0

def modif_Personne():
    takecolumn = 0
    
#la fonction va créer un fichier arbre.db ou écraser l'ancien fichier arbre pour un vierge
creer_tables()

#ouverture de la connexion avec le fichier
conn = sqlite3.connect('arbre.db')
cur = conn.cursor()
cur.execute("""INSERT INTO Personne (id, fname, lname, address)
    VALUES (1, 'DUPONT', 'Jean', '36 rue des coquelicots')""")
conn.commit()

cur.execute("""INSERT INTO Personne (id, fname, lname, address, phone, birthday, fathername, fatherbirthday, motherfirstname, motherlastname, motherbirthday, idfather, idmother)
    VALUES (2, 'DUPONT', 'Jeanne', '36 rue des coquelicots', '0605241558', 24/02/1999, 'DUPONT', 14/05/1950, 'Marie', 'Latour', 26/01/1951, NULL, NULL )""")
conn.commit()

cur.execute("""INSERT INTO Identite (username, password, admin)
    VALUES ('admin', 'gempitoon', 1)""")
conn.commit()

#exemple avecla variable user qui stocke le nom d utilisateur et la variable res qui doit recevoir le mot de passe
user= ('admin',)
res = cur.execute("""SELECT password FROM Identite
    Where username = ? """, user)
print(res.fetchone())
modification('Personne', ('Tonton', 'Paul'), ('fname', 'lname'), 1)
res = cur.execute("""SELECT fname, lname FROM Personne""")
print(res.fetchone())

res = cur.execute("""SELECT * FROM Personne""")
print(res.fetchall())
noeud_suppression('Personne', 1)

res = cur.execute("""SELECT * FROM Personne""")
print(res.fetchall())

#fermeture de la connexion avec le fichier
conn.close()

size_tree()