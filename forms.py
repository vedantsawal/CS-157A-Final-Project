from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired, EqualTo


class UserCreationForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()], render_kw={'autofocus': True})
    password = PasswordField("Password", validators = [DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo('password')])
    first_name = StringField("First Name", validators = [DataRequired()])
    last_name = StringField("Last Name", validators = [DataRequired()])
    phone_number = StringField("Phone Number", validators = [DataRequired()])
    address = StringField("Address", validators = [DataRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()], render_kw={'autofocus': True})
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField()
    
class AddProductsForm(FlaskForm):
    title = StringField("title", validators = [DataRequired()], render_kw={'autofocus': True})
    img_url = StringField("img_url", validators = [DataRequired()])
    caption = StringField("caption", validators = [DataRequired()])
    price = DecimalField("price", validators=[DataRequired()])
    quantity = IntegerField("quantity", validators=[DataRequired()])
    submit = SubmitField()
    
class MakeAdminForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()], render_kw={'autofocus': True})
    submitadmin = SubmitField()