from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class CreateChatForm(FlaskForm):

    chatname = StringField('Chat Name: ',
                             validators=[DataRequired()]
                             )

    submit = SubmitField('Create!')