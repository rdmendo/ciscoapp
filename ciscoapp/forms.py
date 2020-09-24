from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length, Email, EqualTo, IPAddress


choice_priv = open('ciscoapp/text_data/private.txt').read().splitlines()
choice_int = open('ciscoapp/text_data/interface.txt').read().splitlines()

class DhcpForm(FlaskForm):
    network_address = StringField("IPV4 Address", validators= [DataRequired(), IPAddress()])
    pool =  StringField('DHCP Pool',validators=[DataRequired(), Length(min=2, max=20)])
    private_ip = SelectField('Private IP',choices=choice_priv, validators=[DataRequired()])
    interface = SelectField('Interface', choices=choice_int, validators=[DataRequired()])
    submit = SubmitField('Generate')