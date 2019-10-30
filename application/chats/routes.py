from flask import Flask, jsonify, render_template
from flask import request, Blueprint
import sqlalchemy
from application import models, db
from application.models import Message
from flask_login import current_user

ChatsAPI = Blueprint("chats_api", __name__)

@ChatsAPI.route('/<username>/chats', methods=['GET'])
def get_chats(username):

    user = User.query.filter(User.username == username)
    chats = user.chats
    jsonchats = [cht.to_chat() for cht in chats]
    return jsonify(jsonchats), 200

@ChatsAPI.route('/', methods=['POST'])
def create_chat():
    
    try:
        chat = Chat.from_chat(request.json)
    except KeyError as e:
        return jsonify(f'Missing key: {e.args[0]}'), 400

    db.session.add(chat)
    db.session.commit()
    return jsonify(), 200

@ChatsAPI.route('/<chat_id>/add/<username>', methods=['PUT'])
def add_user_to_chat(chat_id, username):
    ...

@ChatsAPI.route('/<chat_id>/remove/<username>', methods=['PUT'])
def delete_user_from_chat(chat_id, username):
    ...

@ChatsAPI.route('/<chat_id>/users', methods=['GET'])
def get_chat_users(chat_id):
    ...
