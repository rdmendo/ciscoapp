from flask import render_template, url_for, flash, redirect, Response, session, request, Blueprint
from ciscoapp import app, db, bcrypt
from ciscoapp.network_automation.forms import DivertForm, RerouteForm
from ciscoapp.api.divert import Divert
from ciscoapp.api.reroute import ISPReroute
from ciscoapp.models import AdvertisedNetwork, Reroute
from datetime import datetime
from nornir.plugins.functions.text import print_result
from flask_login import login_user, current_user, logout_user, login_required

network_automation = Blueprint('network_automation', __name__)

@network_automation.route("/divert", methods=['GET', 'POST'])
@login_required
def divert():
    form = DivertForm()
    # get_network = AdvertisedNetwork.query.all()
    get_network = reversed(AdvertisedNetwork.query.order_by(AdvertisedNetwork.id).all()[-10:])

    if form.validate_on_submit():
        #connections to devices
        user_divert = Divert(form.network.data, form.task.data)
        result = user_divert.nr.run(task=user_divert.advertise_to_incapsula)
        user_divert.nr.close_connections()

        # add form datas to db
        if form.task.data == 'Divert All' or form.task.data == 'No Divert All':
            new = AdvertisedNetwork(prefix="113.61.42 - 58.0/24", task=form.task.data)
            db.session.add(new)
            db.session.commit()
        else:
            new = AdvertisedNetwork(prefix=form.network.data, task=form.task.data)
            db.session.add(new)
            db.session.commit()
            
        # print_result(result)
        
        #variables for flash messages
        hosts = user_divert.nr.inventory.hosts
        failed_host = result.failed_hosts.keys()
        for x in hosts:
            if x in failed_host:
                flash(f"Unsuccessful task in {x}", 'danger')
            else:
                flash(f"Successful task in {x}", 'success')
    
        return redirect(url_for('network_automation.divert', form=form, result=result))
    return render_template('divert.html', title="DDOS", form=form, network=get_network)

@network_automation.route("/reroute", methods=['GET', 'POST'])
@login_required
def reroute():
    form = RerouteForm()
    get_reroute = reversed(Reroute.query.order_by(Reroute.id).all()[-10:])

    if form.validate_on_submit():
        user_reroute = ISPReroute(form.ipaddress.data, form.isp.data)
        result = user_reroute.nr.run(task=user_reroute.reroute)
        user_reroute.nr.close_connections()
        
        new_route = Reroute(ipaddress=f"{form.ipaddress.data}/32", isp=form.isp.data)
        db.session.add(new_route)
        db.session.commit()
        
        flash(f"{form.ipaddress.data} is rerouted to {form.isp.data}", 'success')
        
        return redirect(url_for('network_automation.reroute', form=form))
    return render_template('reroute.html', title="Reroute", form=form, routes=get_reroute)
