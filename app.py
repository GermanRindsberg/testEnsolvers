from os import stat_result
from flask import Flask, json, session, jsonify, request
from flask.typing import StatusCode
from flask_cors import CORS, cross_origin
from back.models.models import db, User, Task, Folder


app = Flask(__name__)
cors= CORS(app)

app.config.from_object("back.config.DevelepmentConfig")
app.config['CORS_HEADERS'] = 'Content-Type'


db.init_app(app)


@app.route("/login", methods=['GET','POST'])
def login():
    try:
        email=request.json['email']
        password= request.json['password']

        user = User.query.filter_by(email=email).first()
    
        
        if user is not None and User.verificarPassword(user,password):
            email=user.email
            return jsonify(
                email = email,
                id=user.id,
                mensaje='Welcome '+email,
                status=200
            )
        else:
             return jsonify(
                mensaje='User or password incorrect',
                status=404
            )
    except Exception as e:
        print(e)
        return jsonify(
            mensaje='Ocurrio un error inesperado',
            status=400
        )

@app.route("/addUser", methods=['POST'])
def addUser():
    try:
        name=request.json['name']
        mail=request.json['email']
        pw=request.json['password']
        user= User(name=name, email=mail, password= User.create_password(pw))
        db.session.add(user)
        db.session.commit()
        return jsonify (
            mensaje='Usuario registrado con exito',
            status=200
        )

    except Exception as e:
        print(e)
        return jsonify(
            mensaje='Ocurrio un error inesperado',
            status=400
        )


@app.route("/getFolders", methods=['GET','POST'])
def getFolders():
    try:
        id=request.json['id']
        folders = db.session.query(Folder).filter(Folder.userId == id).all()
        toReturn=[folder.serialize() for folder in folders]
        if toReturn is not None:
            return jsonify(
                folders = toReturn,
                mensaje='Folders',
                status=200
            )
        else:
             return jsonify(
                mensaje='No Folders',
                status=404
            )
    except Exception as e:
        print(e)
        return jsonify(
            mensaje='Ocurrio un error inesperado haciendo get a las carpetas',
            status=400
        )

@app.route("/addFolder",methods=['POST'])
def addFolder():
    try:
        if request.json['folderName']!='':
            folderName=request.json['folderName']    
            id= request.json['id']    
            user = User.query.filter(User.id == id).first()
            folder= Folder(name=folderName, usuario=user )
            db.session.add(folder)
            db.session.commit()
            return jsonify (
                mensaje='Carpeta registrada con exito',
                status=200
        )
        else:
            return jsonify(
                mensaje='No se pudo crear la carpeta, posiblemente no ingreso un nombre valido',
                status=404
            )
    except Exception as e:
        print(e)
        return jsonify(
            mensaje='Ocurrio un error inesperado sumando una carpeta',
            status=400
        )

@app.route("/delFolder", methods=['POST'])
def delFolder():
    id = request.json['id']
    try:
        if id is not None:
            Folder.query.filter(Folder.id == id).delete()
            Task.query.filter(Task.folderId == id).delete()
            db.session.commit()
            return jsonify (
                mensaje='Carpeta Eliminada con exito',
                status=200
        )
        else:
            return jsonify(
                mensaje='No se pudo crear la carpeta',
                status=404
            )
   
    except Exception as e:
        print(e)
        return jsonify(
            mensaje='Ocurrio un error inesperado',
            status=400
        )


@app.route("/getTasks", methods=['GET','POST'])
def getTasks():
    try:
        id=request.json['id']
        tasks = db.session.query(Task).filter(Task.folderId == id).all()
        toReturn=[Task.serialize(task) for task in tasks]
      
        if toReturn is not None:
            return jsonify(
                tasks = toReturn,
                mensaje='Tasks',
                status=200
            )
       
        else:
             return jsonify(
                mensaje='No Tasks',
                status=404
            )
    except Exception as e:
        print(e)
        return jsonify(
            mensaje='Ocurrio un error inesperado en getTask',
            status=400
        )

@app.route("/delTask", methods=['POST'])
def delTask():
    id = request.json['id']
    try:
        if id is not None:
            Task.query.filter(Task.id == id).delete()
            db.session.commit()
            return jsonify (
                mensaje='Tarea Eliminada con exito',
                status=200
        )
        else:
            return jsonify(
                mensaje='No se pudo eliminar la tarea',
                status=404
            )
   
    except Exception as e:
        print(e)
        return jsonify(
            mensaje='Ocurrio un error inesperado al borrar la tarea',
            status=400
        )


@app.route("/logout")
def logout():
    if session['name']:
       session.clear()
       return jsonify( 
           mensaje='Bye bye',
                status=200)
    else:     
        return jsonify(
            mensaje='Ocurrio un error inesperado',
            status=400
        )

@app.route("/addTask" , methods=['POST'])
def addTask():
    try:
        if request.json['taskName']!='':
            folderId=request.json['idFolder']
            folderName=Folder.query.filter(Folder.id == folderId).first()
            taskName=request.json['taskName']
            task= Task(name=taskName, carpeta=folderName )
            db.session.add(task)
            db.session.commit()
            return jsonify (
                mensaje='Tarea registrada con exito',
                status=200
            )
        else:
            return jsonify(
                mensaje='No se pudo crear la tarea, posiblemente no selecciono una carpeta',
                status=404
            )
    except Exception as e:
        print(e)
        return jsonify(
            mensaje='Ocurrio un error inesperado agregando la tarea',
            status=400
        )


@app.route("/editTask", methods=['POST'])
def editTask():
    try:
        taskName=request.json['taskName']
        taskId=request.json['taskId']
        task = Task.query.filter_by(id=taskId).first()
        task.name=taskName
        db.session.commit() 
        return jsonify(
            mensaje='editado con exito',
            status=200
        )
    except Exception as e:
        print(e)
        return jsonify(
            mensaje='Ocurrio un error inesperado editando la tarea',
            status=400
        )

@app.route("/editFinish", methods=['POST'])
def editFinish():
    try:
        taskId=request.json['taskId']
        task = db.session.query(Task).filter(Task.id == taskId).first()
        if task.finished==1:
            task.finished=0    
        else:    
            task.finished=1
        db.session.commit()
        return jsonify(
            mensaje='editado con exito',
            status=200
        )
    except Exception as e:
        print(e)
        return jsonify(
            mensaje='Ocurrio un error inesperado editando el finish',
            status=400
        )
   

if __name__ =='__main__': 
     app.run()
