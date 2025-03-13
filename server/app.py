from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = []
    if request.method == 'GET':
        for message in Message.query.order_by(Message.created_at.asc()).all():
            message_obj = message.to_dict()
            messages.append(message_obj)
        response = make_response(
            jsonify(messages),
            200
        )
        return response
    
    if request.method == 'POST':
        data = request.get_json()
        #new_resource
        message = Message(
            body = data['body'],
            username = data['username']
        )
        db.session.add(message)
        db.session.commit()
        
        #convert the resource to dict -> JSON
        message_obj = message.to_dict()
        response = make_response(
            jsonify(message_obj),
            201
        )
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)
    
    if request.method == 'PATCH':
        data = request.get_json()
        
        for attr in data:
            setattr(message, attr, data[attr])
        db.session.add(message)
        db.session.commit()
        
        message_obj =message.to_dict()
        response = make_response(
            jsonify(message_obj),
            200
        )
        return response
    
    if request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        
        response_body = {
            'deleted_successfully': True,
            'message': 'Message deleted'
        }
        response = make_response(
            jsonify(response_body),
            200
        )
        return response
   

if __name__ == '__main__':
    app.run(port=5555)
