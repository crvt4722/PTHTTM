import mysql.connector


class Sample:
    def __init__(self, name, filepath, status, labelid):
        self.id = None
        self.name = name
        self.filepath = filepath
        self.status = status
        self.labelid = labelid

    def setID(self, id):
        self.id = id


class SampleDAO:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost", user="root", password="admin", database="pthttm"
        )
        self.cursor = self.db.cursor()

    def getAllSample(self):
        query = "SELECT * FROM sample"
        self.cursor.execute(query)
        rs = self.cursor.fetchall()
        self.cursor.close()
        sampleList = []
        for row in rs:
            sample = Sample(row[1], row[2], row[3], row[4])
            sample.setID(row[0])
            sampleList.append(sample)
        return sampleList

    def findSampleByName(self, name):
        query = "SELECT * FROM sample WHERE name=%s"
        self.cursor.execute(query, (name,))
        rs = self.cursor.fetchall()
        self.cursor.close()
        sampleList = []
        for row in rs:
            sample = Sample(row[1], row[2], row[3], row[4])
            sample.setID(row[0])
            sampleList.append(sample)
        return sampleList

    def findSampleById(self, id):
        query = "SELECT * FROM sample WHERE id=%s"
        self.cursor.execute(query, (id,))
        rs = self.cursor.fetchall()
        self.cursor.close()
        sampleList = []
        for row in rs:
            sample = Sample(row[1], row[2], row[3], row[4])
            sample.setID(row[0])
            sampleList.append(sample)
        return sampleList

    def addSample(self, sample):
        try:
            query = "INSERT INTO sample (name, file_path,status,Labelid) VALUES (%s,%s,%s, %s)"
            self.cursor.execute(
                query,
                (
                    sample.name,
                    sample.filepath,
                    sample.status,
                    sample.labelid,
                ),
            )
            self.db.commit()
            self.cursor.close()
            return True
        except:
            return False

    def updateSample(self, sample, id):
        try:
            query = "UPDATE sample SET name=%s, file_path=%s,status=%s,Labelid=%s WHERE id =%s"
            self.cursor.execute(
                query,
                (
                    sample.name,
                    sample.filepath,
                    sample.status,
                    sample.labelid,
                    id,
                ),
            )
            self.db.commit()
            self.cursor.close()
            return True
        except:
            return False

    def deleteSample(self, id):
        try:
            query = "DELETE FROM sample WHERE id=%s"
            self.cursor.execute(query, (id,))
            self.db.commit()
            self.cursor.close()
            return True
        except:
            return False
