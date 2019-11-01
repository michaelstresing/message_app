from flask import Flask, jsonify, render_template
from flask import request, Blueprint
import sqlalchemy
from application import models, db
from application.models import Message, Chat
from flask_login import current_user

MessageAPI = Blueprint("messages_api", __name__)

@MessageAPI.route('/<chat_id>/messages', methods=['GET'])
def get_messages(chat_id):
    """
    Gets all the messages for a user_id and chat_id
    """
    # userid = str(current_user.get_id())
    chat = Chat.query.filter(Chat.chat_id == chat_id).first()

    # if userid in chat.users:
    #     messagelist = Message.query.filter(
    #                                     Message.chat_id == chat_id
    #                                     ).order_by(Message.timesent).all()
    # else:
    #     return "Not Found", 404

    messagelist = Message.query.filter(
                                Message.chat_id == chat_id
                                ).order_by(Message.timesent.desc()).all()

    if messagelist is None:
        return 'No messages!', 404

    return jsonify([msg.to_messages() for msg in messagelist]), 200


@MessageAPI.route('/<chat_id>/messages', methods=['POST'])
def send_message(chat_id):
    """
    Allows a user to send a message. Takes as arguments chat_id, sender_id and content
    """
    user_id = str(current_user.get_id())
    messagetext = request.json["content"]

    try:
        newmessage = Message.from_messages(messagetext, chat_id, user_id)
    except KeyError as e:
        return jsonify(f'Missing key: {e.args[0]}'), 400

    db.session.add(newmessage)
    db.session.commit()
    return jsonify(newmessage.to_messages()), 200

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