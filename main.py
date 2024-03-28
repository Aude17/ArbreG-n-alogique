import sqlite3
import datetime
# on a besoin de cette bibliothèque pour manipuler sql
# on creer la fonction qui va elle meme creer deux table la premiere qui est la table des element de l arbre
# 1 mother and 0 father
def creer_tables():
    conn = sqlite3.connect('arbre.db')
    cur = conn.cursor()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS Personne (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname TEXT,
    lname TEXT,
    gender boolean,
    address TEXT,
    phone TEXT,
    nationality TEXT,
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
    
    cur.execute("""CREATE TABLE IF NOT EXISTS Identite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    admin INT)""")

    conn.close()


def renitialisation(target):
    conn = sqlite3.connect('arbre.db')
    cur = conn.cursor()
    if target==1:
        cur.execute("DROP TABLE IF EXISTS Personne")
    if target==2:
        cur.execute("DROP TABLE IF EXISTS Identite")
    

def saisir_date():
    while True:
        date_str = input("Entrez une date au format YYYY-MM-DD : ")
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            return date
        except ValueError:
            print("Format de date invalide. Veuillez saisir une date au format YYYY-MM-DD.")


def saisie_boolean():
    while True:
        try:
            valeur = input("Entrez un booléen (True ou False) : ")
            if valeur.lower() == 'true':
                return True
            elif valeur.lower() == 'false':
                return False
            else:
                raise ValueError("Veuillez entrer True ou False.")
        except ValueError as e:
            print(e)



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
            cur.execute("""INSERT INTO Identite (username, password, admin)
                VALUES (?, ?, ?)""", tuple)
            conn.commit()
            conn.close()
            return  True

    elif table == 'Personne':
        if len(tuple)!= 14:
            return False
        else:
            conn = sqlite3.connect('arbre.db')
            cur = conn.cursor()
            cur.execute("""INSERT INTO Personne (fname, lname, gender, address, phone,nationality, birthday, fathername, fatherbirthday, motherfirstname, motherlastname, motherbirthday, idfather, idmother)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,)""", tuple)
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
    

def eleminationPersonne(idtarget):
    conn = sqlite3.connect('arbre.db')
    cur = conn.cursor()
    cur.execute("""DELETE FROM Personne
            WHERE id = ?""", (idtarget,))
    conn.commit()
    conn.close()


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



def show(firstname, lastname):
    conn = sqlite3.connect('arbre.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM Personne
                      where fname = ? OR lname = ?""", (firstname, lastname,))
    res= cur.fetchall()
    conn.close()
    return res



def suppression_descendance():
    takeuname = input("Entrez le prenom de la personne: ")
    take2name = input("Entrez le nom de famille")
    res = show('Personne', takeuname, take2name)
    print("La liste de personne possible")
    for i in range(len(res)):
        print(res[i][1]+' '+ res[i][2]+' son id) : '+res[i][0])
    
    print('Choisissez une des cible potentiel')
    takepass = input('Choisissez une des cible potentiel')
    verif = False
    while verif == False:
        takepass = input('Choisissez une des cible potentiel')
        for ligne in res:
            if ligne[0] == takepass:
                verif = True
                break
        if verif:
            break
        else:
            print("veuillez choisir parmi les id propose")

    fin =noeud_suppression('Personne', takepass)
    return fin




# rajouter la saisi au clavier avec variable saisis et verifpass pour enregistrer les valeurs saisi.
def connexion():
    while True:
        username = input("Entrez le nom d'utilisateur : ")
        password = input("Entrez le mot de passe : ")

        conn = sqlite3.connect('arbre.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM Identite WHERE username = ? AND password = ?", (username, password))
        result = cur.fetchone()
        conn.close()

        if result:
            if result[2] == 1:
                return False
            return True
        else:
            print("Nom d'utilisateur ou mot de passe incorrect.")


def insertion_Personne():
    validation = False
    while validation == False:
        print("Vous allez saisir les information de la personne, si certaine information sont inconnu veuillez rien remplir et pasez à la suivante.")

        firstname = input("Le prénom de la personne : ")
        lastname = input("Le nom de famille : ")
        print("Le sexe de la Personne True pour une femme false sinon ")
        sex= saisie_boolean()
        address = input(" L'addresse de sont lieu d'habitation: ")
        telefon = input(" le numéro de téléphone: ")
        national = input("La ntionalité de la personne: ")
        birth = saisir_date()
        fathname = None
        fathbirthday = None
        mothname = None
        mothbirthday = None
        mothlasstname = None
        idfath = None
        idmoth = None

        print("Valider vous la saisi ?")
        print(firstname+' '+lastname+' ,est une femme : '+sex+' la personne vie au '+address+' et est de nationalité: '+national+ ' la personne est né le :'+birth)
        validation = saisie_boolean

    #validation va être utiliser dans le reste de la fonction ouisqu'ellle à fait son rôle avant
    print(' la personne à des parents ?')
    if( saisie_boolean() == True):
        takeuname = input("Entrez le prenom de la personne: ")
        take2name = input("Entrez le nom de famille")
        res = show('Personne', takeuname, take2name)
        result = [ line for line in res if res[4] == True]
        





def modif_Personne():
    takecolumn = 0
    return False


#la fonction va créer un fichier arbre.db ou écraser l'ancien fichier arbre pour un vierge
renitialisation(1)
renitialisation(2)
creer_tables()

#ouverture de la connexion avec le fichier
conn = sqlite3.connect('arbre.db')
cur = conn.cursor()
cur.execute("""INSERT INTO Personne (fname, lname, address)
    VALUES ('DUPONT', 'Jean', '36 rue des coquelicots')""")
conn.commit()

cur.execute("""INSERT INTO Personne (fname, lname, address, phone, birthday, fathername, fatherbirthday, motherfirstname, motherlastname, motherbirthday, idfather, idmother)
    VALUES ('DUPONT', 'Jeanne', '36 rue des coquelicots', '0605241558', 24/02/1999, 'DUPONT', 14/05/1950, 'Marie', 'Latour', 26/01/1951, NULL, NULL )""")
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

insertion('Identite', ('Jean', 'Pierre', 0))

#fermeture de la connexion avec le fichier
conn.close()
#res =connexion()

#eleminationPersonne(2)
#res = show( 'Dupont', 'Jeanne')
print(res)
size_tree()
