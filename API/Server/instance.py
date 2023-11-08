from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Configurar o Flask-RESTx
api = Api(app, version='1.0', title='API de Exemplo', description='Exemplo de API com Flask-RESTx')

# Definir o modelo da tabela
resource_fields = api.model('Resource', {
    'id': fields.Integer,
    'nome': fields.String,
    'idade': fields.Integer
})

# Definir o modelo do banco de dados
class Tabela(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80))
    idade = db.Column(db.Integer)

db.create_all()

@api.route('/create')
class CreateResource(Resource):
    @api.expect(resource_fields)
    def post(self):
        data = request.json
        nome = data['nome']
        idade = data['idade']

        new_record = Tabela(nome=nome, idade=idade)
        db.session.add(new_record)
        db.session.commit()
        return {'message': 'Registro criado com sucesso'}, 201

@api.route('/read')
class ReadResource(Resource):
    def get(self):
        records = Tabela.query.all()
        result = [{'id': record.id, 'nome': record.nome, 'idade': record.idade} for record in records]
        return result

@api.route('/update/<int:id>')
class UpdateResource(Resource):
    @api.expect(resource_fields)
    def put(self, id):
        data = request.json
        nome = data['nome']
        idade = data['idade']

        record = Tabela.query.get(id)
        if not record:
            api.abort(404, 'Registro não encontrado')

        record.nome = nome
        record.idade = idade
        db.session.commit()
        return {'message': f'Registro com ID {id} atualizado com sucesso'}

@api.route('/delete/<int:id>')
class DeleteResource(Resource):
    def delete(self, id):
        record = Tabela.query.get(id)
        if not record:
            api.abort(404, 'Registro não encontrado')

        db.session.delete(record)
        db.session.commit()
        return {'message': f'Registro com ID {id} excluído com sucesso'}

if __name__ == '__main__':
    app.run(debug=True)
