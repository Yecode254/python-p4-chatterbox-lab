from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# ROUTES

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return make_response(jsonify([m.to_dict() for m in messages]), 200)

@app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    try:
        message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(message)
        db.session.commit()
        return make_response(message.to_dict(), 201)
    except Exception as e:
        return make_response({'error': str(e)}, 400)

@app.route('/messages/<int:id>', methods=['PATCH'])
def patch_message(id):
    message = Message.query.filter_by(id=id).first()
    if not message:
        return make_response({'error': 'Message not found'}, 404)

    data = request.get_json()
    if 'body' in data:
        message.body = data['body']
    db.session.commit()
    return make_response(message.to_dict(), 200)

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.filter_by(id=id).first()
    if not message:
        return make_response({'error': 'Message not found'}, 404)

    db.session.delete(message)
    db.session.commit()
    return make_response('', 204)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
