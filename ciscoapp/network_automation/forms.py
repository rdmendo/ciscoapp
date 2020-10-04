from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Length, Email, EqualTo, IPAddress, ValidationError

choice_task =  open('ciscoapp/text_data/divert_task.txt').read().splitlines()
choice_allowed_ip = open('ciscoapp/text_data/allowed_network.txt').read().splitlines()
choice_isp = open('ciscoapp/text_data/isp.txt').read().splitlines()

class DivertForm(FlaskForm):
    # network =  StringField("Network", validators= [DataRequired(), IPAddress()])
    network = SelectField('Network', choices=choice_allowed_ip, validators=[DataRequired()])
    task =  SelectField('Task',choices=choice_task, validators=[DataRequired()])
    submit = SubmitField('Mitigate')
    
class RerouteForm(FlaskForm):
    ipaddress = StringField("Website IP Address", validators= [DataRequired(), IPAddress()])
    isp =  SelectField('Route to',choices=choice_isp, validators=[DataRequired()])
    submit = SubmitField('Reroute')
    
