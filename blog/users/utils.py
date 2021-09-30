import os
import secrets
from blog import mail
from flask import url_for, current_app
from PIL import Image
from flask_mail import Message

print(os.path.dirname(os.path.realpath(__file__)))


def save_picture(form_picture): 
    print(dir(form_picture)) # if the data is file. then there are new kinds of property for access, such as .filename and save
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.split(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    #resizing
    output_size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    #  _external it means an absolute URL instead of an relative URL, as this is not within our app already
    msg.body=f"""To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignoret his email no changes will be made.

"""
    mail.send(msg)

