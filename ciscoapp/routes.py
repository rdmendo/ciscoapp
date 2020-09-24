from flask import render_template, url_for, flash, redirect
from ciscoapp import app
from ciscoapp.forms import DhcpForm
from ciscoapp.generators.scripts.dhcp import GenerateDhcp


@app.route("/",  methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    
@app.route("/dhcp", methods=['GET', 'POST'])
def dhcp():
    form = DhcpForm()
    if form.is_submitted():
        user_dhcp = GenerateDhcp(form.network_address.data, form.pool.data,form.interface.data, form.private_ip.data)
        result = user_dhcp.create_pool()
        
        return render_template('dhcp.html', result=result, form=form)
        
    return render_template('dhcp.html', form=form)