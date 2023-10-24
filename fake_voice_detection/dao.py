import mysql.connector

mydb = mysql.connector.connect(user='crvt4722',password='04072002',host='localhost',database='fake_voice_detection')
mycursor = mydb.cursor()

# Insert new Model and set it as the default Model when perform train or retrain model.
def insertModel(
        name = '',
        file_path = '',
        accuracy = 0, precision = 0, f1_score = 0 , recall = 0,
        description = '',
        sample_quantity = 0
):

    # Get the sample quantity in order to check the condition to retrain model in the future.
    sql = 'SELECT COUNT(*) FROM Sample;'
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    sample_quantity = myresult[0][0]

    # Insert the new Model to database.
    sql = ('INSERT INTO Model(name, file_path, training_date, accuracy,`precision`, recall, `f1_score`, description, status, sample_quantity) '
           ' VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s, 1, %s);')

    print(sql)
    val = (name, file_path, accuracy, precision, recall, f1_score, description, sample_quantity)
    mycursor.execute(sql, val)
    mydb.commit()

# Function to get all samples and label from the database.
def getAllSamples():
    sql = 'SELECT Sample.file_path, Label.value FROM Sample, Label WHERE Labelid = Label.id'
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return myresult
    # for i in myresult:
    #     print(i[0], i[1])

# Function to get the last model's id in order to prevent model's name conflictions.
def getLastModelId():
    sql = 'SELECT id FROM Model ORDER BY id DESC'
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return myresult[0][0]

# getAllSamples()
# insertModel()