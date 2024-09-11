from flask_ckeditor import CKEditorField
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired,URL,Email
from flask_wtf import FlaskForm

class Register(FlaskForm):
    name=StringField("NAME", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(),])
    password=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField('SIGN-up')

class Login(FlaskForm):
    email=StringField("Email",validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit=SubmitField('SIGN-in')

class CarBlog(FlaskForm):
    car_name=StringField("Car-Name", validators=[DataRequired()])
    car_company=StringField("Car-Company", validators=[DataRequired()])
    engine=StringField("Engine-Typ", validators=[DataRequired()])
    max_speed=StringField("Max-speeed",validators=[DataRequired()])
    Time=StringField("Time to reach 200 ", validators=[DataRequired()])
    power=StringField("Max-power", validators=[DataRequired()])
    img_url = StringField("Image", validators=[DataRequired(), URL()])
    blog=CKEditorField("Content",validators=[DataRequired()])
    submit=SubmitField("ADD")


class EditBlogForm(FlaskForm):
    car_name = StringField('Car Name', validators=[DataRequired()])
    car_company = StringField('Car Company', validators=[DataRequired()])
    engine = StringField('Engine', validators=[DataRequired()])
    max_speed = StringField('Top Speed', validators=[DataRequired()])
    Time = StringField('Time to 200 km/h', validators=[DataRequired()])
    power = StringField('Power Output', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired()])
    blog = CKEditorField('Blog Content', validators=[DataRequired()])
    submit = SubmitField('Save Changes')
