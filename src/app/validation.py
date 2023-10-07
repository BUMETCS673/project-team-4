from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    firstName = StringField('firstName', validators=[
            validators.DataRequired(message='First name should not be empty!')
        ],)
    lastName = StringField('lastName', validators=[
            validators.DataRequired(message='last name should not be empty!')
        ],)
    email = StringField('email', [validators.Email(message="Not an email address")])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.Length(min=8,max=32,message='password must be between 8 and 32 characters long'),
        
    ])
    confirm_password = PasswordField('confirm_password',[validators.EqualTo('password', message='Password must match')])

