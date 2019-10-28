from flask import Flask, jsonify, render_template
from flask import request, Blueprint
import sqlalchemy
from .config import Config
from . import db
from application import models

MessageAPI = Blueprint("messages_api", __name__)
@MessageAPI.route('/api/chats/<group_id>/messages?user_id=<user_id>', methods=['GET'])
def get_messages():
    """
    Gets all the messages for a user_id and chat_id
    """

    result = db.session.execute(
        '''
        SELECT m.id, m.group_id, m.sender_id, m.content, m.created_at, m.updated_at FROM messages AS m INNER JOIN group_users AS gu ON gu.group_id = m.group_id WHERE m.group_id = :group_id AND gu.user_id = :user_id'
        '''
        , {group_id: group_id, user_id: user_id })
    result = to_message(result)

@MessageAPI.route('/api/chats/<group_id>/messages?user_id=<user_id>', methods=['POST'])
def send_message():
    """
    Allows a user to send a message
    """
    #
    if request.json: # If there is data in the POST request
        data = request.json.to_message()

        result = db.session.execute(
            '''
            INSERT INTO messages AS m (m.group_id, m.sender_id, m.content) VALUES (:group_id, :sender_id, :content
            '''
        ,{group_id: data['group_id'], sender_id: data['sender_id'], content: data['content']})
    return "Created new message "
















