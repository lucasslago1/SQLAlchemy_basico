from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  #Registrando o Flask 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db" #Registrando o banco de dados em app.db
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #Desabilitando o warning

db = SQLAlchemy(app) #Registrando o SQLAlchemy(obrigatório para qualquer import)

class User(db.Model): #User herda da classe Model
    __tablename__ = "users" #Tabela do bd
    #Criando colunas
    id = db.Column(db.Integer, primary_key=True) #Coluna id do tipo inteiro
    name = db.Column(db.String(84), nullable=False)  #Coluna name do tipo String com o máximo de 84 caracteres, sem aceitar valor nulo
    email = db.Column(db.String(84), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)

    def __str__(self):
        return self.name

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Unicode(124), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


    def __str__(self):
        return self.name

@app.route("/")
def index():
    users = User.query.all() # Select * from users; 
    return render_template("users.html", users=users)

@app.route("/user/<int:id>") 
def unique(id):
    user = User.query.get(id)
    return render_template("user.html", user=user)

@app.route("/user/delete/<int:id>") #Rota para deletar usuário
def delete(id):
    user = User.query.filter_by(id=id).first()  #Consulta o id do usuário
    db.session.delete(user)  #Deleta
    db.session.commit() #Grava no banco a ação

    return redirect("/")  #Redireciona para a página inicial


if __name__ == "__main__":
    app.run(debug=True)