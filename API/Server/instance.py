from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db = SQLAlchemy(app)

class Dado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    valor = db.Column(db.String(100))

@app.route('/', methods=['POST'])
def adicionar_dado():
    data = request.json
    nome = data['nome']
    valor = data['valor']

    novo_dado = Dado(nome=nome, valor=valor)
    db.session.add(novo_dado)
    db.session.commit()

    return jsonify({'message': 'Dado adicionado com sucesso'}), 201

@app.route('/buscar_dados', methods=['GET'])
def buscar_dados():
    dados = Dado.query.all()
    resultado = [{'nome': dado.nome, 'valor': dado.valor} for dado in dados]
    return jsonify(resultado)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
