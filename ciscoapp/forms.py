from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Length, Email, EqualTo, IPAddress


choice_priv = open('ciscoapp/text_data/private.txt').read().splitlines()
choice_int = open('ciscoapp/text_data/interface.txt').read().splitlines()
choice_dev = open('ciscoapp/text_data/device.txt').read().splitlines()
choice_int_qos = open('ciscoapp/text_data/interface_qos.txt').read().splitlines()
choice_level = open('ciscoapp/text_data/level.txt').read().splitlines()
choice_implem = open('ciscoapp/text_data/implementation.txt').read().splitlines()
choice_task =  open('ciscoapp/text_data/divert_task.txt').read().splitlines()
choice_allowed_ip = open('ciscoapp/text_data/allowed_network.txt').read().splitlines()

class DhcpForm(FlaskForm):
    network_address = StringField("IPV4 Address", validators= [DataRequired(), IPAddress()])
    pool =  StringField('DHCP Pool',validators=[DataRequired(), Length(min=2, max=20)])
    private_ip = SelectField('Private IP',choices=choice_priv, validators=[DataRequired()])
    interface = SelectField('Interface', choices=choice_int, validators=[DataRequired()])
    submit = SubmitField('Generate')
    
class QOSForm(FlaskForm):
    policy_name =  StringField('Policy Name',validators=[DataRequired(), Length(min=2, max=20)])
    bandwidth = IntegerField('Bandwidth', validators=[DataRequired()])
    device = SelectField('Device Type',choices=choice_dev, validators=[DataRequired()])
    interface = SelectField('Interface', choices=choice_int_qos, validators=[DataRequired()])
    submit = SubmitField('Generate')
    
class NewForm(FlaskForm):
    implementation_type = SelectField('Implementation Type',choices=choice_implem, validators=[DataRequired()])
    name =  StringField('Office Name',validators=[DataRequired(), Length(min=2, max=20)])
    network = StringField("IPV4 Address", validators= [DataRequired(), IPAddress()])
    bandwidth = IntegerField('Bandwidth', validators=[DataRequired()])
    inet = IntegerField('Inet Vlan', validators=[DataRequired()])
    level = SelectField('Floor Level',choices=choice_level, validators=[DataRequired()])
    interface = SelectField('Interface', choices=choice_int_qos, validators=[DataRequired()])
    submit = SubmitField('Generate')
    
class AddForm(FlaskForm):
    existing_link =  StringField("Existing Uplink", validators= [DataRequired(), IPAddress()])
    new_link = StringField("New IP Address", validators= [DataRequired()])
    submit = SubmitField('Generate')
    
class DivertForm(FlaskForm):
    # network =  StringField("Network", validators= [DataRequired(), IPAddress()])
    network = SelectField('Network', choices=choice_allowed_ip, validators=[DataRequired()])
    task =  SelectField('Task',choices=choice_task, validators=[DataRequired()])
    submit = SubmitField('Mitigate')
    