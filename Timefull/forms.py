from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField, PasswordField, FloatField, EmailField, DateField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired(), Length(min=5, message="Username needs at least 5 characters!")])
    password1  = PasswordField("Password: ", validators=[DataRequired(), Length(min=5, message="Password needs at least 5 characters!")])
    password2  = PasswordField("Confirm Password: ", validators=[DataRequired(), Length(min=5, message="Password needs at least 5 characters!"), EqualTo('password1', message='Passwords need to match!!')])
    submit = SubmitField("Submit")
    
#doesnt need validators maybe?
#I did them in app.py anyways 
class LoginForm(FlaskForm):
    username = StringField("Username: ")
    password  = StringField("Password: ")
    submit = SubmitField("Submit")

#i dont think this needs validation
class EditPriceForm(FlaskForm):
    attribute = SelectField('Product', choices=[
        ('Sharpy', 'Sharpy'),
        ('Pinky', 'Pinky'),
        ('Timey', 'Timey'),
        ('Wakey', 'Wakey'),
        ('Bitey', 'Bitey'),
        ('Whimey', 'Whimey'),
        ('Sparky', 'Sparky')])
    price  = FloatField("New Price: ", default="15.45")
    submit = SubmitField("Submit")

#same here
class ReviewForm(FlaskForm):
    attribute = SelectField('Product', choices=[
        ('Sharpy', 'Sharpy'),
        ('Pinky', 'Pinky'),
        ('Timey', 'Timey'),
        ('Wakey', 'Wakey'),
        ('Bitey', 'Bitey'),
        ('Whimey', 'Whimey'),
        ('Sparky', 'Sparky')])
    
    review_text = TextAreaField('Review')

    rating = SelectField('Rating', choices=[
        ('One', 'One'),
        ('Two', 'Two'),
        ('Three', 'Three'),
        ('Four', 'Four'),
        ('Five', 'Five')])
    
    submit = SubmitField("Submit")

#
class PaymentForm(FlaskForm):
    #is this racist? I dont wanna discriminate against Wu Lee
    firstname = StringField("First Name: ", validators=[DataRequired(), Length(min=2, message="Name needs at least 2 characters!")])
    surname  = StringField("Surname: ", validators=[DataRequired(), Length(min=2, message="Username needs at least 2 characters!")])
    email = EmailField("Email Address: ", validators=[Email()])
    postcode = StringField("Postcode: ", validators=[DataRequired()])

    card_number = StringField("Card Number", validators=[DataRequired(), Length(min=16, max=16, message="INVALID CARD LENGTH")])
    #yay luhn mod method time, we will do half the validation here and half over there I think, this one just checks length :)
    
    expiry_date = DateField("Expiry Date: ")

    CCV = IntegerField("CCV", validators=[DataRequired(),NumberRange(min=0, max=999, message="INVALID NUMBER ")])
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    attribute = SelectField('Product', choices=[
        ('All', 'All'),
        ('C', 'Clocks'),
        ('W', 'Watches')])
    min_price  = StringField("Minimum Price € ", default="0")
    max_price  = StringField("Maximum Price € ", default="999")
    submit = SubmitField("Search")

class EditStockForm(FlaskForm):
    attribute = SelectField('Product', choices=[
        ('Sharpy', 'Sharpy'),
        ('Pinky', 'Pinky'),
        ('Timey', 'Timey'),
        ('Wakey', 'Wakey'),
        ('Bitey', 'Bitey'),
        ('Whimey', 'Whimey'),
        ('Sparky', 'Sparky')])
    stock  = IntegerField("New Stock Count: ", default=10)
    submit = SubmitField("Edit")

class ContactForm(FlaskForm):
    attribute = SelectField('Issue', choices=[
        ('Bug', 'Report A Bug'),
        ('Request', 'Request A Refund'),
        ('Missing', 'I have not recieved my item'),
        ('Other', 'Other')])
    
    contact_text = TextAreaField('Please provide any information pertaining to your issue.')

    
    submit = SubmitField("Submit")