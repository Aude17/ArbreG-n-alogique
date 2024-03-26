import sqlite3

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

    conn = sqlite3.connect('arbre.db')
    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS Identite""")
    cur.execute("""CREATE TABLE Identite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    admin INT)""")
    conn.close()

def insertion(table, tuple):
    conn = sqlite3.connect('arbre.db')
    cur = conn.cursor()
    if table == 'Identite':
        if len(tuple) != 2:
            return False
        else:
            cur.execute("""INSERT INTO Identite (username, password)
                VALUES (?, ?)""", tuple)
            conn.commit()
            conn.close()
            return True

    elif table == 'Personne':
        if len(tuple) != 12:
            return False
        else:
            cur.execute("""INSERT INTO Personne (fname, lname, address, phone, birthday, fathername, fatherbirthday, motherfirstname, motherlastname, motherbirthday, idfather, idmother)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", tuple)
            conn.commit()
            conn.close()
            return True
    else:
        return False

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
        res = cur.execute(f"""SELECT id FROM {table}
            WHERE idmother = ? OR idfather = ?""", (idtarget, idtarget))
        for i in res:
            noeud_suppression(table, i[0])
        return True
    return False

def show(tables, idtarget):
    return False

creer_tables()

conn = sqlite3.connect('arbre.db')
cur = conn.cursor()
cur.execute("""INSERT INTO Personne (id, fname, lname, address)
    VALUES (1, 'DUPONT', 'Jean', '36 rue des coquelicots')""")
conn.commit()

cur.execute("""INSERT INTO Personne (id, fname, lname, address, phone, birthday, fathername, fatherbirthday, motherfirstname, motherlastname, motherbirthday, idfather, idmother)
    VALUES (2, 'DUPONT', 'Jeanne', '36 rue des coquelicots', '0605241558', '1999-02-24', 'DUPONT', '1950-05-14', 'Marie', 'Latour', '1951-01-26', NULL, NULL )""")
conn.commit()

cur.execute("""INSERT INTO Identite (username, password, admin)
    VALUES ('admin', 'jesuisdebile', 1)""")
conn.commit()

insertion('Personne', ('Doe', 'John', '123 rue de la Liberté', '0123456789', '1990-01-01', 'Doe Sr.', '1950-05-10', 'Jane', 'Doe', '1960-03-15', None, None))

user = ('admin',)
res = cur.execute("""SELECT password FROM Identite
    Where username = ? """, user)
print(res.fetchone())
modification('Personne', ('Tonton', 'Paul'), ('fname', 'lname'), 1)
res = cur.execute("""SELECT fname, lname FROM Personne""")
print(res.fetchone())

conn.commit()
conn.close()
