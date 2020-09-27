from flask import render_template, url_for, flash, redirect, Response
from ciscoapp import app
from ciscoapp.forms import DhcpForm, QOSForm, NewForm, AddForm
from ciscoapp.generators.scripts.configenerate import GenerateDhcp , GenerateQos, GenerateCloudware, GenerateAdditional
from datetime import datetime

@app.route("/",  methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    
@app.route("/dhcp", methods=['GET', 'POST'])
def dhcp():
    form = DhcpForm()
    if form.is_submitted():
        user_dhcp = GenerateDhcp()
        result = user_dhcp.create_pool(form.network_address.data, form.pool.data,form.interface.data, form.private_ip.data)
        poolcount = user_dhcp.count_pool(form.network_address.data)
        
        flash(f"{poolcount} dhcp pool has been created with network  {form.network_address.data} for {form.pool.data.upper()} office.", 'success')
        return render_template('dhcp.html',form=form, result=result )
    return render_template('dhcp.html',title="Dhcp", form=form)

@app.route("/qos", methods=['GET', 'POST'])
def qos():
    form = QOSForm()
    
    if form.validate_on_submit():
        user_qos = GenerateQos()
        result = user_qos.create_qos(form.policy_name.data.upper(), form.bandwidth.data, form.interface.data, form.device.data)
        
        flash(f"QOS Policy has been created for {form.policy_name.data.upper()} {form.bandwidth.data} MBPS", 'success')
        return render_template('qos.html', form=form, result=result)
    return render_template('qos.html',title="Qos", form=form)


@app.route("/new", methods=['GET', 'POST'])
def new():
    form = NewForm()
    
    if form.is_submitted():
        user_new = GenerateCloudware()
        result = user_new.create_office(form.name.data.upper(), form.level.data, form.inet.data, form.network.data, form.interface.data, form.bandwidth.data, form.implementation_type.data)
        
        flash(f"New {form.implementation_type.data} config has been created at {form.level.data} for {form.name.data.upper()} office", 'success')
        return render_template('new.html', form=form, result=result)
    return render_template('new.html',title="New Office", form=form)


@app.route("/additional", methods=['GET', 'POST'])
def additional():
    form = AddForm()
    
    if form.validate_on_submit():
        user_add = GenerateAdditional()
        result = user_add.create_additional(form.new_link.data, form.existing_link.data)
        
        flash(f"New IP Address {form.new_link.data} config has been created and will be routed back to existing link {form.existing_link.data}.", 'success')
        return render_template('additional.html', form=form, result=result)
    return render_template('additional.html',title="Additional IP", form=form)
