from flask import render_template, url_for, flash, redirect, Response, session, request
from ciscoapp import app, db, bcrypt
from ciscoapp.forms import DhcpForm, QOSForm, NewForm, AddForm, DivertForm, RerouteForm, LoginForm, RegistrationForm
from ciscoapp.generators.scripts.configenerate import GenerateDhcp , GenerateQos, GenerateCloudware, GenerateAdditional
from ciscoapp.generators.scripts.divert import Divert
from ciscoapp.generators.scripts.reroute import ISPReroute
from ciscoapp.models import AdvertisedNetwork, Reroute, User
from datetime import datetime
from nornir.plugins.functions.text import print_result
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/",  methods=['GET', 'POST'])
def index():
    get_network = reversed(AdvertisedNetwork.query.order_by(AdvertisedNetwork.id).all()[-10:])
    return render_template('index.html', network=get_network)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()

    if form.is_submitted():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return  redirect (next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

    
@app.route("/dhcp", methods=['GET', 'POST'])
@login_required
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
@login_required
def qos():
    form = QOSForm()
    
    if form.validate_on_submit():
        user_qos = GenerateQos()
        result = user_qos.create_qos(form.policy_name.data.upper(), form.bandwidth.data, form.interface.data, form.device.data)
        
        flash(f"QOS Policy has been created for {form.policy_name.data.upper()} {form.bandwidth.data} MBPS", 'success')
        return render_template('qos.html', form=form, result=result)
    return render_template('qos.html',title="Qos", form=form)


@app.route("/new", methods=['GET', 'POST'])
@login_required
def new():
    form = NewForm()
    
    if form.is_submitted():
        user_new = GenerateCloudware()
        result = user_new.create_office(form.name.data.upper(), form.level.data, form.inet.data, form.network.data, form.interface.data, form.bandwidth.data, form.implementation_type.data)
        
        flash(f"New {form.implementation_type.data} config has been created at {form.level.data} for {form.name.data.upper()} office", 'success')
        return render_template('new.html', form=form, result=result)
    return render_template('new.html',title="New Office", form=form)


@app.route("/additional", methods=['GET', 'POST'])
@login_required
def additional():
    form = AddForm()
    
    if form.validate_on_submit():
        user_add = GenerateAdditional()
        result = user_add.create_additional(form.new_link.data, form.existing_link.data)
        
        flash(f"New IP Address {form.new_link.data} config has been created and will be routed back to existing link {form.existing_link.data}.", 'success')
        return render_template('additional.html', form=form, result=result)
    return render_template('additional.html',title="Additional IP", form=form)

@app.route("/divert", methods=['GET', 'POST'])
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
            
        print_result(result)
        
        #variables for flash messages
        hosts = user_divert.nr.inventory.hosts
        failed_host = result.failed_hosts.keys()
        for x in hosts:
            if x in failed_host:
                flash(f"Unsuccessful task in {x}", 'danger')
            else:
                flash(f"Successful task in {x}", 'success')
    
        return redirect(url_for('divert', form=form, result=result))
    return render_template('divert.html', title="DDOS", form=form, network=get_network)

@app.route("/reroute", methods=['GET', 'POST'])
@login_required
def reroute():
    form = RerouteForm()
    get_reroute = reversed(Reroute.query.order_by(Reroute.id).all()[-10:])

    if form.validate_on_submit():
        user_reroute = ISPReroute(form.ipaddress.data, form.isp.data)
        result = user_reroute.nr.run(task=user_reroute.reroute)
        user_reroute.nr.close_connections()
        
        hosts = user_reroute.nr.inventory.hosts
        failed_host = result.failed_hosts.keys()
        
        for x in hosts:
            if x in failed_host and x == 'CORE-R1' or x == 'CORE-R2' and form.isp.data == 'ETPI':
                flash(f"Connection ERROR to {x} ---> {form.ipaddress.data}/32 is NOT routed to {form.isp.data}", 'danger')
                
            elif x in failed_host and x == 'CORE-R1' or x == 'CORE-R2' and form.isp.data == 'GLOBE':
                flash(f"Connection ERROR to {x} ---> {form.ipaddress.data}/32 is NOT routed to {form.isp.data}", 'danger')
                
            elif x in failed_host and x == 'CORE-R1' or x == 'CORE-R2' and form.isp.data == 'CONVERGE':
                flash(f"Connection ERROR to {x} ---> {form.ipaddress.data}/32 is NOT routed to {form.isp.data}", 'danger')
                
                
        print_result(result)
    # add to database tables
        new_route = Reroute(ipaddress=f"{form.ipaddress.data}/32", isp=form.isp.data)
        db.session.add(new_route)
        db.session.commit()
        
        return redirect(url_for('reroute', form=form))
    return render_template('reroute.html', title="Reroute", form=form, routes=get_reroute)

    


    
    
    


    
        