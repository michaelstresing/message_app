from flask import Flask, jsonify, render_template
from flask import request, Blueprint
import sqlalchemy
from application import models, db
from application.models import Message

MessageAPI = Blueprint("messages_api", __name__)

@MessageAPI.route('/chats/<chat_id>/messages', methods=['GET'])
def get_messages(chat_id):
    """
    Gets all the messages for a user_id and chat_id
    """

    result = db.session.execute(
        '''
        SELECT 
          m.message_id
         ,m.chat_id
         ,m.sender_id
         ,m.content
         ,m.timesent 
        FROM 
          messages AS m 
        INNER JOIN 
          chat_users AS gu 
        ON 
          gu.chat_id = m.chat_id 
        WHERE 
          m.chat_id = :chat_id 
        AND 
          gu.user_id = :user_id'
        '''
        , {chat_id: chat_id, user_id: request.args['user_id'] })
    db.session.commit()
    return jsonify(result.to_messages())


@MessageAPI.route('/chats/<chat_id>/messages', methods=['POST'])
def send_message(chat_id):
    """
    Allows a user to send a message. Takes as arguments ChatID, SenderID and Content
    """
    #
    if request.json: # If there is data in the POST request
        message = Message.from_messages(request.json, chat_id, request.args['user_id'])

        result = db.session.execute(
            '''
            INSERT INTO 
              messages (chat_id, sender_id, content) 
            VALUES 
              (:chat_id, :sender_id, :content)
            '''
        , dict(chat_id=chat_id, sender_id=request.args['user_id'], content=message.content))
        db.session.commit()
    return "Created new Message"