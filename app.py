from flask import Flask,url_for,render_template,request,redirect,url_for,session,flash, jsonify
from sample import SampleDAO, Sample
from user import UserDAO, User
from label import LabelDAO
from model import Model
from modelDAO import ModelDAO
from functools import wraps
from ServiceDAO import  ServiceDAO
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "pthttm"


@app.errorhandler(404)
def notFound(e):
    return render_template("404.html")

def checkUserLogin(func):
    @wraps(func)
    def inner(*arg,**kwargs):
        if session.__contains__('username'):
            return func(*arg,**kwargs)
        else:
            return redirect('/')
    return inner

def checkAdminLogin(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.__contains__("role"):
            if session["role"] == 1:
                return func(*args, **kwargs)
            else:
                return render_template("404.html")
        else:
            return redirect("/")

    return inner


@app.route("/home")
@checkUserLogin
def home():
    session['detect_upload'] = ''
    return render_template("home_main.html")


@app.route("/home_record")
@checkUserLogin
def home_record():
    return render_template("home_record.html")


@app.route("/home_upload")
@checkUserLogin
def home_upload():    
    return render_template("home_upload.html")

#upload file
app.config['UPLOAD_FOLDER'] = 'Sounds'  # Thư mục lưu trữ tệp tải lên

@app.route('/upload', methods=['POST'])
@checkUserLogin
def upload_file():
    
    result = ''
    if 'audio_data' not in request.files:
        result =  'Không có tệp nào được tải lên.'

    file = request.files['audio_data']

    if file.filename == '':
        result =  'Không có tệp nào được chọn'

    if file:
        filename = session['username']+'.wav'  # Tên tệp lưu trữ (sound.wav)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        file_path = 'Sounds/'  + filename
        service_DAO = ServiceDAO()
        voice_detect = service_DAO.fake_voice_detection(file_path)

        os.remove(file_path)

        if voice_detect == '1':   
            result = 'Giọng nói thật'
        else: result = 'Giọng nói giả mạo'
          

    session['detect_upload'] = result
    return redirect("home_upload")        

@app.route('/record', methods = ['POST'])
@checkUserLogin
def record_result():    
    result = ''
    if 'audio_data' not in request.files:
        result =  'Không có tệp nào được tải lên.'

    file = request.files['audio_data']

    if file.filename == '':
        result =  'Không có tệp nào được chọn'

    if file:
        filename = session['username']+'.wav'  # Tên tệp lưu trữ (sound.wav)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        file_path = 'Sounds/'  + filename
        service_DAO = ServiceDAO()
        voice_detect = service_DAO.fake_voice_detection(file_path)

        os.remove(file_path)

        if voice_detect == '1':   
            result = 'Giọng nói thật'
        else: result = 'Giọng nói giả mạo'
          

    session['detect_upload'] = result
    print(session['detect_upload'] )
    return redirect("home_record")    

@app.route("/manager")
@checkAdminLogin
def manager():
    return render_template("manager.html")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        userDAO = UserDAO()
        user = userDAO.login(username, password)
        if user:
            # if user.role=='1':
            session["username"] = user.username
            session["role"] = user.role
            if session["role"] == 1:
                return redirect(url_for("manager"))
            else:
                return redirect(url_for("home"))
        else:
            flash("Username or password is wrong", "warning")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fullname = request.form["fullname"]
        username = request.form["username"]
        password = request.form["password"]
        repassword = request.form["re-password"]
        if password != repassword:
            flash("Invalid Password", "warning")
        else:
            uer = User(username, password, fullname, role="0")
            userDAO = UserDAO()
            ok = userDAO.signup(uer)
            if ok:
                return redirect(url_for("login"))
            else:
                flash("Account registration failed", "warning")
    return render_template("signup.html")


# sample


@app.route("/manager-sample", methods=["GET", "POST"])
@checkAdminLogin
def managerSample():
    if request.method == "POST":
        name = request.form["key"]
        sampleDAO = SampleDAO()
        sampleList = sampleDAO.findSampleByName(name)
        if sampleList:
            return render_template("managerSample.html", sampleList=sampleList)
        else:
            flash("Sample not found", "warning")
    sampleDAO = SampleDAO()
    sampleList = sampleDAO.getAllSample()
    return render_template("managerSample.html", sampleList=sampleList)

@app.route("/train-retrain")
@checkAdminLogin
def train_retrain():
    sampleDAO = SampleDAO()
    sampleList = sampleDAO.getAllSample()
    return render_template("train_retrain.html", sampleList=sampleList)

@app.route("/manager-sample/add", methods=["POST", "GET"])
@checkAdminLogin
def add():
    if request.method == "POST":
        name = request.form["name"]
        filepath = request.form["filepath"]
        status = "0"
        labelId = request.form["labelid"]
        sample = Sample(name, filepath, status, labelId)
        sampleDAO = SampleDAO()
        ok = sampleDAO.addSample(sample)
        if ok:
            flash("Insert successful!", "success")
            return redirect(url_for("managerSample"))
        else:
            flash("Insert was not successful", "error")
    return render_template("addSample.html")


@app.route("/manager-sample/edit/<int:id_data>", methods=["POST", "GET"])
@checkAdminLogin
def edit(id_data):
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        filepath = request.form["filepath"]
        status = "0"
        labelId = request.form["labelid"]
        sample = Sample(name, filepath, status, labelId)
        sampleDAO = SampleDAO()
        ok = sampleDAO.updateSample(sample, id)
        if ok:
            flash("Update successful!", "success")
            return redirect(url_for("managerSample"))
        else:
            flash("Update was not successful", "error")
    sampleDAO = SampleDAO()
    sample = sampleDAO.findSampleById(id_data)
    return render_template("editSample.html", sample=sample)


@app.route("/manager-sample/delete/<int:id>", methods=["GET", "POST"])
@checkAdminLogin
def delete(id):
    sampleDAO = SampleDAO()
    ok = sampleDAO.deleteSample(id)
    if ok:
        flash("Delete successful!", "success")
        return redirect(url_for("managerSample"))
    else:
        flash("Delete was not successful", "error")


# label


@app.route("/manager-label", methods=["GET", "POST"])
@checkAdminLogin
def managerLabel():
    if request.method == "POST":
        key = request.form["key"]
        labelDAO = LabelDAO()
        label = labelDAO.findLabelByName(key)
        if label:
            return render_template("managerLabel.html", label=label)
        else:
            flash("Label not found", "warning")
    # Thực hiện truy vấn SQL để lấy dữ liệu nếu biến query_data là True
    labelDAO = LabelDAO()
    label = labelDAO.getAllLabel()
    return render_template("managerLabel.html", label=label)


@app.route("/manager-label/insert", methods=["POST"])
@checkAdminLogin
def insertLabel():
    if request.method == "POST":
        name = request.form["name"]
        value = request.form["value"]
        labelDAO = LabelDAO()
        ok = labelDAO.insertLabel(name, value)
        if ok:
            return redirect(url_for("managerLabel"))


@app.route("/manager-label/editLabel", methods=["POST", "GET"])
@checkAdminLogin
def editLabel():
    if request.method == "POST":
        id_data = request.form["id"]
        name = request.form["name"]
        value = request.form["value"]
        labelDAO = LabelDAO()
        ok = labelDAO.updateLabel(name, value, id_data)
        if ok:
            return redirect(url_for("managerLabel"))


@app.route("/manager-label/delete/<string:id_data>", methods=["GET"])
@checkAdminLogin
def deleteLabel(id_data):
    labelDAO = LabelDAO()
    ok = labelDAO.deleteLabel(id_data)
    if ok:
        return redirect(url_for("managerLabel"))


# model


@app.route("/manager-model", methods=["GET", "POST"])
@checkAdminLogin
def modelHome():
    dao = ModelDAO()
    if request.method == "POST":
        if request.form.__contains__("str") and request.form["str"] != "":
            return render_template(
                "modelHome.html",
                models=dao.searchByName(request.form["str"]),
                activeModel=dao.getActiveModel(),
            )
        if (request.form.__contains__('start-date') and  request.form.__contains__('end-date')
            and request.form["start-date"] != "" and request.form["end-date"] != "") :
            return render_template(
                "modelHome.html",
                models=dao.searchByTime(request.form["start-date"],request.form["end-date"]),
                activeModel=dao.getActiveModel(),
            )
    return render_template(
        "modelHome.html", models=dao.getAllModel(), activeModel=dao.getActiveModel()
    )


@app.route("/manager-model/<int:id>")
@checkAdminLogin
def modelDetail(id):
    dao = ModelDAO()
    return render_template("modelDetail.html", model=dao.getModel(id))


@app.route("/manager-model/update/<int:id>", methods=["POST"])
@checkAdminLogin
def updateModel(id):
    dao = ModelDAO()
    model = Model()
    model.id = id
    model.name = request.form["name"]
    model.path = request.form["path"]
    mess = dao.updateModel(model)
    flash(mess)
    return redirect(f"/manager-model/{id}")


@app.route("/manager-model/delete/<int:id>")
@checkAdminLogin
def deleteModel(id):
    dao = ModelDAO()
    mess = dao.deleteModel(id)
    flash(mess)
    return redirect("/manager-model")


@app.route("/manager-model/active/<int:id>")
@checkAdminLogin
def activeModel(id):
    dao = ModelDAO()
    mess = dao.activeModel(id)
    flash(mess)
    return redirect(f"/manager-model/{id}")

@app.route("/manager-model/train-retrain", methods = ['POST', 'GET'])
@checkAdminLogin
def trainRetrainModel():
    
    
    data = request.get_json()    
    samples = data.get('samples')

    samples = list(samples)
    print(samples)
    
    # flash('This operation can take a few minutes!')
    service_DAO = ServiceDAO()
    service_DAO.train_or_retrain(samples = samples)
    flash('Train model successfully!')
    return redirect(f"/manager-model")




if __name__ == "__main__":
    app.run(debug=True)
