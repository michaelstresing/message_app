from flask import Flask, jsonify, render_template
from flask import request, Blueprint
import sqlalchemy
from application import models, db
from application.models import Message

MessageAPI = Blueprint("messages_api", __name__)

@MessageAPI.route('/<chat_id>/messages', methods=['GET'])
def get_messages(chat_id):
    """
    Gets all the messages for a user_id and chat_id
    """
    userid = request.args["user_id"]
    messagelist = Message.query.filter(Message.chat_id == chat_id, Message.sender_id == userid).all()
    if messagelist is None:
        return 'No messages!', 404
    return jsonify([msg.to_messages() for msg in messagelist]), 200


@MessageAPI.route('/<chat_id>/messages', methods=['POST'])
def send_message(chat_id):
    """
    Allows a user to send a message. Takes as arguments chat_id, sender_id and sender
    """
    #
    if request.json: # If there is data in the POST request
        message = Message.from_messages(request.json, chat_id, request.args['id'])

        db.session.execute(
            '''
            INSERT INTO 
              messages (chat_id, sender_id, content) 
            VALUES 
              (:chat_id, :sender_id, :content)
            ON CONFLICT DO NOTHING
            '''
        , dict(chat_id=chat_id, sender_id=request.args['id'], content=message.content)
        )
        db.session.commit()
        return "Created new Message"
    else:
        return "Error"

@MessageAPI.route('/<chat_id>/messages', methods=['DELETE'])
def delete_message(chat_id):
    """
    Delete a message.
    """
    if request.json:
        for row in request.json:
            message = Message.from_messages(row, chat_id, request.args['id'])
            db.session.execute(
                '''
                DELETE FROM
                  messages
                WHERE
                  message_id = :message_id
                '''
                , dict(message_id=message.message_id)
            )
        db.session.commit()
        return "Successfully deleted message"
    else:
        return "Error"