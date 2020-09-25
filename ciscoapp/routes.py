from flask import render_template, url_for, flash, redirect
from ciscoapp import app
from ciscoapp.forms import DhcpForm, QOSForm
from ciscoapp.generators.scripts.dhcp import GenerateDhcp
from ciscoapp.generators.scripts.qos import GenerateQos


@app.route("/",  methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    
@app.route("/dhcp", methods=['GET', 'POST'])
def dhcp():
    form = DhcpForm()
    
    if form.is_submitted():
        user_dhcp = GenerateDhcp(form.network_address.data, form.pool.data,form.interface.data, form.private_ip.data)
        result = user_dhcp.create_pool()
        poolcount = user_dhcp.count_pool()
        flash(f"{poolcount} dhcp pool has been created with network  {form.network_address.data} for {form.pool.data.upper()} office.", 'success')
        
        return render_template('dhcp.html',form=form, result=result )
    return render_template('dhcp.html', form=form)

@app.route("/qos", methods=['GET', 'POST'])
def qos():
    form = QOSForm()
    
    if form.validate_on_submit():
        user_qos = GenerateQos(form.policy_name.data.upper(), form.bandwidth.data, form.interface.data, form.device.data)
        result = user_qos.create_qos()
        flash(f"QOS Policy has been created for {form.policy_name.data.upper()} {form.bandwidth.data} MBPS", 'success')
        
        return render_template('qos.html', form=form, result=result)
    return render_template('qos.html', form=form)