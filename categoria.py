from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from sqlalchemy.orm.exc import ConcurrentModificationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/bdpythonapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
ma = Marshmallow(app)


#creación de tabla categoria
class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key = True)
    cat_nom =  db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))

    def __init__(self,cat_nom, cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp

db.create_all()

#esquema categoria
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nom', 'cat_desp')

#una sola respuesta
categoria_schema = CategoriaSchema()
#cuando sean muchas respuestas
categorias_schema = CategoriaSchema(many=True)

class Login(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    correo = db.Column(db.String(100))  
    pasw = db.Column(db.String(100))

    def __init__(self, correo, pasw):
        self.correo = correo
        self.pasw = pasw
db.create_all()

class LoginSchema(ma.Schema):
    class Meta:
        fields = ('correo', 'pasw')

login_schema = LoginSchema()
logins_schema = LoginSchema(many=True)

#get
@app.route('/categoria', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

#get por id
@app.route('/categoria/<id>', methods=['GET'])
def get_categorias_id(id):
    una_categoria = Categoria.query.get(id)#tomar solo el registro indicado en la petición por id
    return categoria_schema.jsonify(una_categoria)
#metodo post

@app.route('/categoria', methods=['POST'])
def insert_categorias():
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']
    nuevo_registro=Categoria(cat_nom,cat_desp)
    db.session.add(nuevo_registro)
    db.session.commit()
    return categoria_schema.jsonify(nuevo_registro)
@app.route('/login',methods=['GET'])
def get_login():
    all_user = Login.query.all()
    result = logins_schema.dump(all_user)
    return jsonify(result)

@app.route('/login',methods=['POST'])
def insert_user():
    data = request.get_json(force=True)#forzando a que el request sea json
    correo = data['correo']
    pasw = data['pasw']
    nuevo_usuario = Login(correo,pasw)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return login_schema.jsonify(nuevo_usuario)

#mensaje de bienvenida
@app.route('/',methods=['GET'])
def index():
    return jsonify({'Mensaje':'Bienvendo'})

if __name__=="__main__":
    app.run(debug=True)