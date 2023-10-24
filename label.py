import mysql.connector


class Label:
    def __init__(self, id, name, value):
        self.id = id
        self.name = name
        self.value = value


class LabelDAO:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost", user="root", password="admin", database="pthttm"
        )
        self.cursor = self.db.cursor()

    def getAllLabel(self):
        query = "SELECT * FROM label"
        self.cursor.execute(query)
        rs = self.cursor.fetchall()
        self.cursor.close()
        label = []
        for row in rs:
            label.append(Label(row[0], row[1], row[2]))
        return label

    def findLabelByName(self, name):
        query = "SELECT * FROM label WHERE name=%s"
        self.cursor.execute(query, (name,))
        rs = self.cursor.fetchall()
        self.cursor.close()
        label = []
        for row in rs:
            label.append(Label(row[0], row[1], row[2]))
        return label

    def findLabelById(self, id):
        query = "SELECT * FROM label WHERE id=%s"
        self.cursor.execute(query, (id,))
        rs = self.cursor.fetchall()
        self.cursor.close()
        label = []
        for row in rs:
            label.append(Label(row[0], row[1], row[2]))
        return label

    def addLabel(self, name, value):
        try:
            query = "INSERT INTO label (name, value) VALUES (%s,%s,%s, %s)"
            self.cursor.execute(
                query,
                (
                    name,
                    value,
                ),
            )
            self.db.commit()
            self.cursor.close()
            return True
        except:
            return False

    def updateLabel(self, name, value):
        try:
            query = "UPDATE label SET name=%s, value=%s WHERE id =%s"
            self.cursor.execute(query, (name, value, id))
            self.db.commit()
            self.cursor.close()
            return True
        except:
            return False

    def deleteLabel(self, id):
        try:
            query = "DELETE FROM label WHERE id=%s"
            self.cursor.execute(query, (id,))
            self.db.commit()
            self.cursor.close()
            return True
        except:
            return False

    def findLabelById(self, id):
        query = "SELECT * FROM label WHERE id=%s"
        self.cursor.execute(query, (id,))
        rs = self.cursor.fetchall()
        self.cursor.close()
        label = []
        for row in rs:
            label.append(Label(row[0], row[1], row[2]))
        return label

    def insertLabel(self, name, value):
        try:
            query = "INSERT INTO label (name, value) VALUES (%s,%s)"
            self.cursor.execute(
                query,
                (
                    name,
                    value,
                ),
            )
            self.db.commit()
            self.cursor.close()
            return True
        except:
            return False

    def updateLabel(self, name, value, id):
        try:
            query = "UPDATE label SET name=%s, value=%s WHERE id =%s"
            self.cursor.execute(query, (name, value, id))
            self.db.commit()
            self.cursor.close()
            return True
        except:
            return False

    def deleteLabel(self, id):
        try:
            query = "DELETE FROM label WHERE id=%s"
            self.cursor.execute(query, (id,))
            self.db.commit()
            self.cursor.close()
            return True
        except:
            return False
