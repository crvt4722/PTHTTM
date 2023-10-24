import mysql.connector
from model import Model

host = "localhost"
user = "crvt4722"
password = "04072002"
database = "fake_voice_detection"


class ModelDAO:
    _tableName = "model"

    def __init__(self):
        self.db = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        self.db.autocommit = True

    def getAllModel(self):
        q = f"select * from {self._tableName}"
        cursor = self.db.cursor()
        cursor.execute(q)
        lst = [Model(i) for i in cursor.fetchall()]
        cursor.close()
        return lst

    def searchByName(self, s):
        q = f"select * from {self._tableName} where name like '%{s}%' or file_path like '%{s}%'"
        cursor = self.db.cursor()
        cursor.execute(q)
        lst = [Model(i) for i in cursor.fetchall()]
        cursor.close()
        return lst

    def getModel(self, id):
        q = f"select * from {self._tableName} where id={id}"
        cursor = self.db.cursor()
        cursor.execute(q)
        model = Model(cursor.fetchone())
        cursor.close()
        return model

    def getActiveModel(self):
        q = f"select * from {self._tableName} where status=1 limit 1"
        cursor = self.db.cursor()
        cursor.execute(q)
        model = Model(cursor.fetchone())
        cursor.close()
        return model

    def updateModel(self, model):
        if (
            model.name == ""
            or model.name == None
            or model.path == ""
            or model.path == "None"
        ):
            return "Invalid model!"
        if not self.checkValidModel(model):
            return "Model name or path already exists!"
        q = f"update {self._tableName} set name='{model.name}', file_path='{model.path}' where id={model.id}"
        cursor = self.db.cursor()
        cursor.execute(q)
        cursor.close()
        return "Update successful!"

    def deleteModel(self, id):
        q = f"delete from {self._tableName} where id={id}"
        cursor = self.db.cursor()
        cursor.execute(q)
        cursor.close()
        return "Delete successful!"

    def activeModel(self, id):
        q1 = f"update {self._tableName} set status=0"
        q2 = f"update {self._tableName} set status=1 where id={id}"
        cursor = self.db.cursor()
        cursor.execute(q1)
        cursor.execute(q2)
        cursor.close()
        return "Active model successful!"
    
    def searchByTime(self,st,en):
        q=f"select * from {self._tableName} where training_date between \'{st}\' and \'{en}\'"
        cursor = self.db.cursor()
        cursor.execute(q)
        lst = [Model(i) for i in cursor.fetchall()]
        cursor.close()
        return lst

    def checkValidModel(self, model):
        q = f"select count(*) from {self._tableName} where not id='{model.id}' and ( name='{model.name}' or file_path='{model.path}' )"
        cursor = self.db.cursor()
        cursor.execute(q)
        return cursor.fetchone()[0] == 0
