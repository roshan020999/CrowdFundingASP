import os

from flask import Flask, request, render_template, session, redirect
import pymysql
app = Flask(__name__)
app.secret_key = "energy"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = APP_ROOT + "/static"

conn = pymysql.connect(host="localhost", user="root", password="998971@momS", db="CrowdFunding")
cursor = conn.cursor()

status_seeker_Request = "Seeker Raise Request"
status_hospital_accepted = "Accepted by Hospital"
status_seeker_cancelled = "Cancelled by Seeker"
status_hospital_rejected = "Rejected by Hospital"
status_admin_accepted = "Accepted by Admin"
status_admin_rejected = "Rejected by Admin"
status_verifier_accepted = "Accepted by Verifier"
status_verifier_rejected = "Rejected by Verifier"
status_amount_donated = "Total Amount Donated"


count = cursor.execute("select *from bankAccount")
if count == 0:
    cursor.execute("insert into bankAccount(account_number,account_balance,account_holder) values('345672897612', '0','Administrator')")
    conn.commit()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/adminLogin")
def adminLogin():
    return render_template("adminLogin.html")


@app.route("/adminLogin1", methods=['post'])
def adminLogin1():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == 'admin' and password == 'admin':
        session['role'] = 'Admin'
        return redirect("/adminHome")
    else:
        return render_template("msg.html", message="Invalid Login Details", color="bg-danger text-white")


@app.route("/adminHome")
def adminHome():
    return render_template("adminHome.html")


@app.route("/location")
def location():
    cursor.execute("select * from location")
    locations = cursor.fetchall()
    return render_template("location.html", locations=locations)


@app.route("/addLocation")
def addLocation():
    return render_template("addLocation.html")


@app.route("/addLocation1", methods=['post'])
def addLocation1():
    location_name = request.form.get("location_name")
    cursor.execute("insert into location(location_name) values('" + str(location_name) + "')")
    conn.commit()
    return redirect("/location")


@app.route("/verifier")
def verifier():
    cursor.execute("select * from verifier")
    verifiers = cursor.fetchall()
    return render_template("verifier.html", verifiers=verifiers, get_location_id=get_location_id)


@app.route("/addVerifier")
def addVerifier():
    cursor.execute("select * from location")
    locations = cursor.fetchall()
    return render_template("addVerifier.html", locations=locations)


@app.route("/addVerifier1", methods=['post'])
def addVerifier1():
    verifier_name = request.form.get("verifier_name")
    verifier_email = request.form.get("verifier_email")
    verifier_phone = request.form.get("verifier_phone")
    verifier_password = request.form.get("verifier_password")
    verifier_address = request.form.get("verifier_address")
    location_id = request.form.get("location_id")

    cursor.execute("insert into verifier(verifier_name,verifier_email,verifier_phone,verifier_password,verifier_address,location_id) values('" + str(verifier_name) + "','" + str(verifier_email) + "','" + str(verifier_phone) + "','" + str(verifier_password) + "','" + str(verifier_address) + "','" + str(location_id) + "')")
    conn.commit()
    return redirect("/verifier")


def get_location_id(location_id):
    cursor.execute("select * from location where location_id='" + str(location_id) + "'")
    location = cursor.fetchall()
    return location[0]


@app.route("/hospitalLogin")
def hospitalLogin():
    return render_template("hospitalLogin.html")


@app.route("/hospitalLogin1", methods=['post'])
def hospitalLogin1():
    email = request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute("select * from hospitals where email = '"+str(email)+"' and password = '"+str(password)+"'")
    if count > 0:
        hospitals = cursor.fetchall()
        hospital = hospitals[0]
        if hospital[8] == "Authorised":
            session['hospital_id'] = hospital[0]
            session['role'] = "Hospital"
            return redirect("/hospitalHome")
        else:
            return render_template("msg.html", message="Hospital is Unauthorised", color="bg-danger text-white")

    else:
        return render_template("msg.html", message="Invalid Login Details", color="bg-danger text-white")


@app.route("/hospitalHome")
def hospitalHome():
    return render_template("hospitalHome.html")


@app.route("/hospitalRegistration")
def hospitalRegistration():
    cursor.execute("select * from location")
    locations = cursor.fetchall()
    return render_template("hospitalRegistration.html", locations=locations)


@app.route("/hospitalRegister1", methods=['post'])
def hospitalRegister1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    hospital_type = request.form.get("hospital_type")
    hospital_code = request.form.get("hospital_code")
    account_number = request.form.get("account_number")
    address = request.form.get("address")
    location_id = request.form.get("location_id")

    cursor.execute("insert into hospitals(name,email,phone,password,hospital_type,hospital_code,address,status,location_id) values('" + str(name) + "','" + str(email) + "','" + str(phone) + "','" + str(password) + "','" + str(hospital_type) + "','" + str(hospital_code) + "','" + str(address) + "','Unauthorised','" + str(location_id) + "')")

    hospital_id = cursor.lastrowid
    cursor.execute("insert into bankAccount(account_number,account_balance,account_holder,hospital_id) values('" + str(account_number) + "','0','Hospital','" + str(hospital_id) + "')")
    conn.commit()
    return render_template("msg.html", message="Hospital Registered Successfully", color="bg-success text-white")


@app.route("/viewHospitals")
def viewHospitals():
    cursor.execute("select * from hospitals")
    hospitals = cursor.fetchall()
    return render_template("viewHospitals.html", hospitals=hospitals,get_location_id=get_location_id)


@app.route("/activateHospital")
def activateHospital():
    hospital_id = request.args.get("hospital_id")
    cursor.execute("update hospitals set status ='Authorised' where hospital_id='" + str(hospital_id) + "'")
    conn.commit()
    return redirect("/viewHospitals")


@app.route("/inactivateHospital")
def inactivateHospital():
    hospital_id = request.args.get("hospital_id")
    cursor.execute("update hospitals set status ='Unauthorised' where hospital_id='" + str(hospital_id) + "'")
    conn.commit()
    return redirect("/viewHospitals")


@app.route("/seekerLogin")
def seekerLogin():
    return render_template("seekerLogin.html")


@app.route("/seekerLogin1", methods=['post'])
def seekerLogin1():
    email = request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute("select * from seekers where email = '"+str(email)+"' and password = '"+str(password)+"'")
    if count > 0:
        seekers = cursor.fetchall()
        seeker = seekers[0]
        if seeker[5] == "Authorised":
            session['seeker_id'] = seeker[0]
            session['role'] = "Seeker"
            return redirect("/seekerHome")
        else:
            return render_template("msg.html", message="Seeker is Unauthorised", color="bg-danger text-white")

    else:
        return render_template("msg.html", message="Invalid Login Details", color="bg-danger text-white")


@app.route("/seekerHome")
def seekerHome():
    return render_template("seekerHome.html")


@app.route("/seekerRegistration")
def seekerRegistration():
    cursor.execute("select * from location")
    locations = cursor.fetchall()
    return render_template("seekerRegistration.html", locations=locations)


@app.route("/seekerRegistration1", methods=['post'])
def seekerRegistration1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    location_id = request.form.get("location_id")

    cursor.execute("insert into seekers(name,email,phone,password,status,location_id) values('" + str(name) + "','" + str(email) + "','" + str(phone) + "','" + str(password) + "','Unauthorised','" + str(location_id) + "')")
    conn.commit()
    return render_template("msg.html", message="Seeker Registered Successfully", color="bg-success text-white")


@app.route("/viewSeekers")
def viewSeekers():
    cursor.execute("select * from seekers")
    seekers = cursor.fetchall()
    return render_template("viewSeekers.html", seekers=seekers, get_location_id=get_location_id)


@app.route("/activateSeeker")
def activateSeeker():
    seeker_id = request.args.get("seeker_id")
    cursor.execute("update seekers set status ='Authorised' where seeker_id='" + str(seeker_id) + "'")
    conn.commit()
    return redirect("/viewSeekers")


@app.route("/inactivateSeeker")
def inactivateSeeker():
    seeker_id = request.args.get("seeker_id")
    cursor.execute("update seekers set status ='Unauthorised' where seeker_id='" + str(seeker_id) + "'")
    conn.commit()
    return redirect("/viewSeekers")


@app.route("/raiseFundRequest")
def raiseFundRequest():
    cursor.execute("select * from hospitals")
    hospitals = cursor.fetchall()
    return render_template("raiseFundRequest.html", hospitals=hospitals)


@app.route("/raiseFundRequest1", methods=['post'])
def raiseFundRequest1():
    seeker_id = session['seeker_id']
    hospital_id = request.form.get("hospital_id")
    cause = request.form.get("cause")
    required_amount = request.form.get("required_amount")

    upload_photo = request.files.get("upload_photo")
    path = APP_ROOT + "/images/" + upload_photo.filename
    upload_photo.save(path)

    upload_reports = request.files.get("upload_reports")
    path = APP_ROOT + "/reports/" + upload_reports.filename
    upload_reports.save(path)

    description = request.form.get("description")

    cursor.execute("insert into raise_request(hospital_id,seeker_id,cause,required_amount,upload_photo,upload_reports,description,status,date) values('" + str(hospital_id) + "','" + str(seeker_id) + "','" + str(cause) + "','" + str(required_amount) + "','" + str(upload_photo.filename) + "','" + str(upload_reports.filename) + "','" + str(description) + "','Seeker Raise Request',now())")
    conn.commit()
    return render_template("msg.html", message="Seeker Raise Request Successfully", color="bg-success text-white")


@app.route("/viewFundRequest")
def viewFundRequest():
    cursor.execute("select * from raise_request")
    if session['role'] == "Hospital":
        cursor.execute("select * from raise_request where status != '" + str(status_seeker_cancelled) + "'")
        conn.commit()
    elif session['role'] == "Admin":
        cursor.execute("select * from raise_request where status != '" + str(status_seeker_Request) + "'  and status != '" + str(status_hospital_rejected) + "'")
        conn.commit()
    elif session['role'] == "Verifier":
        cursor.execute("select * from raise_request where status != '" + str(status_seeker_Request) + "' and status != '" + str(status_seeker_cancelled) + "' and status != '" + str(status_hospital_rejected) + "' and status != '" + str(status_hospital_accepted)+ "' and verifier_id = '" + str(session['verifier_id'])+ "'")
        conn.commit()
    elif session['role'] == "Donor":
        query ="select * from raise_request where status != '" + str(status_seeker_Request) + "'  and status != '" + str(status_seeker_cancelled) + "' and status != '" + str(status_hospital_rejected) + "' and status != '" + str(status_hospital_accepted) + "' and status != '" + str(status_verifier_rejected) + "'"
        raise_request_id = request.args.get("raise_request_id")
        remaining_amount = request.args.get("remaining_amount")
        if remaining_amount == 0:
            cursor.execute("update raise_request set status ='" + str(status_amount_donated) + "' where raise_request_id='" + str(raise_request_id) + "'")
            print("update raise_request set status ='" + str(status_amount_donated) + "' where raise_request_id='" + str(raise_request_id) + "'")
            conn.commit()
        if raise_request_id is not None:
            query = "select * from raise_request where raise_request_id='"+str(raise_request_id)+"'"
        cursor.execute(query)
        conn.commit()
    raise_requests = cursor.fetchall()
    return render_template("viewFundRequest.html", float=float, int=int, get_raise_request_by_raise_request_id=get_raise_request_by_raise_request_id, raise_requests=raise_requests, get_hospital_id=get_hospital_id, get_seeker_id=get_seeker_id)


def get_raise_request_by_raise_request_id(raise_request_id):
    cursor.execute("select sum(amount) from donations where raise_request_id='"+str(raise_request_id)+"' and receiver='Hospital'")
    donations = cursor.fetchall()

    return donations[0][0]


def get_hospital_id(hospital_id):
    cursor.execute("select * from hospitals where hospital_id= '" + str(hospital_id) + "'")
    hospital = cursor.fetchall()
    return hospital[0]


def get_seeker_id(seeker_id):
    cursor.execute("select * from seekers where seeker_id= '" + str(seeker_id) + "'")
    seeker = cursor.fetchall()
    return seeker[0]


@app.route("/cancelSeekerRequest")
def cancelSeekerRequest():
    raise_request_id = request.args.get("raise_request_id")
    cursor.execute("update raise_request set status ='"+str(status_seeker_cancelled)+"' where raise_request_id='" + str(raise_request_id) + "'")
    conn.commit()
    return redirect("/viewFundRequest")


@app.route("/acceptSeekerRequest")
def acceptSeekerRequest():
    raise_request_id = request.args.get("raise_request_id")
    cursor.execute("update raise_request set status ='"+str(status_hospital_accepted)+"' where raise_request_id='" + str(raise_request_id) + "'")
    conn.commit()
    return redirect("/viewFundRequest")


@app.route("/rejectSeekerRequest")
def rejectSeekerRequest():
    raise_request_id = request.args.get("raise_request_id")

    cursor.execute("update raise_request set status ='"+str(status_hospital_rejected)+"' where raise_request_id='" + str(raise_request_id) + "'")
    conn.commit()
    return redirect("/viewFundRequest")


@app.route("/acceptByAdmin")
def acceptByAdmin():
    raise_request_id = request.args.get("raise_request_id")
    cursor.execute("select * from verifier")
    verifiers = cursor.fetchall()
    return render_template("acceptByAdmin.html", verifiers=verifiers, raise_request_id=raise_request_id)


@app.route("/acceptByAdmin1", methods=['post'])
def acceptByAdmin1():
    raise_request_id = request.form.get("raise_request_id")
    verifier_id = request.form.get("verifier_id")
    cursor.execute("update raise_request set status ='"+str(status_admin_accepted)+"' , verifier_id ='"+str(verifier_id)+"' where raise_request_id='" + str(raise_request_id) + "'")
    conn.commit()
    return redirect("/viewFundRequest")


@app.route("/rejectByAdmin")
def rejectByAdmin():
    raise_request_id = request.args.get("raise_request_id")
    cursor.execute("update raise_request set status ='"+str(status_admin_rejected)+"' where raise_request_id='" + str(raise_request_id) + "'")
    conn.commit()
    return redirect("/viewFundRequest")


@app.route("/acceptByVerifier")
def acceptByVerifier():
    raise_request_id = request.args.get("raise_request_id")
    cursor.execute("update raise_request set status ='"+str(status_verifier_accepted)+"' where raise_request_id='" + str(raise_request_id) + "'")
    conn.commit()
    return redirect("/viewFundRequest")


@app.route("/rejectByVerifier")
def rejectByVerifier():
    raise_request_id = request.args.get("raise_request_id")
    cursor.execute("update raise_request set status ='"+str(status_verifier_rejected)+"' where raise_request_id='" + str(raise_request_id) + "'")
    conn.commit()
    return redirect("/viewFundRequest")


@app.route("/verifierLogin")
def verifierLogin():
    return render_template("verifierLogin.html")


@app.route("/verifierLogin1", methods=['post'])
def verifierLogin1():
    verifier_email = request.form.get("verifier_email")
    verifier_password = request.form.get("verifier_password")
    count = cursor.execute("select * from verifier where verifier_email = '" + str(verifier_email) + "' and verifier_password = '" + str(verifier_password) + "'")
    if count > 0:
        verifiers = cursor.fetchall()
        verifier = verifiers[0]
        session['verifier_id'] = verifier[0]
        session['role'] = "Verifier"
        return redirect("/verifierHome")
    else:
        return render_template("msg.html", message="Invalid Login Details", color="bg-danger text-white")


@app.route("/verifierHome")
def verifierHome():
    return render_template("verifierHome.html")


@app.route("/donorLogin")
def donorLogin():
    return render_template("donorLogin.html")


@app.route("/donorLogin1", methods=['post'])
def donorLogin1():
    email = request.form.get("email")
    password = request.form.get("password")
    count = cursor.execute(
        "select * from donor where email = '" + str(email) + "' and password = '" + str(password) + "'")
    if count > 0:
        donors = cursor.fetchall()
        donor = donors[0]
        session['donor_id'] = donor[0]
        session['role'] = "Donor"
        return redirect("/donorHome")

    else:
        return render_template("msg.html", message="Invalid Login Details", color="bg-danger text-white")


@app.route("/donorHome")
def donorHome():
    return render_template("donorHome.html")


@app.route("/donorRegistration")
def donorRegistration():
    cursor.execute("select * from location")
    locations = cursor.fetchall()
    return render_template("donorRegistration.html", locations=locations)


@app.route("/donorRegistration1", methods=['post'])
def donorRegistration1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    location_id = request.form.get("location_id")

    cursor.execute("insert into donor(name,email,phone,password,location_id) values('" + str(name) + "','" + str(email) + "','" + str(phone) + "','" + str(password) + "','" + str(location_id) + "')")
    conn.commit()
    return render_template("msg.html", message="Donor Registered Successfully", color="bg-success text-white")


@app.route("/donateFund")
def donateFund():
    return render_template("donateFund.html")


@app.route("/donateFund1", methods=['post'])
def donateFund1():
    amount = request.form.get("amount")
    cursor.execute("insert into donations(sender,receiver,amount,donation_type,date,donor_id) values('Donor', 'Administrator', '"+str(amount)+"', 'Crowd Fund', now(), '" + str(session['donor_id'])+ "')")
    conn.commit()
    cursor.execute("update bankAccount set account_balance = account_balance + '"+str(amount)+"' where account_holder = 'Administrator'")
    conn.commit()
    return render_template("msg.html", message="Amount Donated Successfully", color="bg-success text-white")


@app.route("/donateAmountForCause")
def donateAmountForCause():
    raise_request_id = request.args.get("raise_request_id")
    cursor.execute("select * from raise_request where raise_request_id = '"+str(raise_request_id)+"'")
    raise_request = cursor.fetchone()
    required_amount = request.args.get("required_amount")
    amount = request.args.get("amount")
    remaining_amount = request.args.get("remaining_amount")
    return render_template("donateAmountForCause.html",remaining_amount=remaining_amount, float=float, raise_request=raise_request, required_amount=required_amount, amount=amount)


@app.route("/donateAmountForCause1", methods=['post'])
def donateAmountForCause1():
    remaining_amount = request.form.get("remaining_amount")
    raise_request_id = request.form.get("raise_request_id")
    hospital_id = request.form.get("hospital_id")
    amount = request.form.get("amount")
    cursor.execute("insert into donations(sender,receiver,amount,donation_type,date,donor_id,raise_request_id) values('Donor', 'Administrator', '" + str(amount) + "', 'Cause', now(), '" + str(session['donor_id']) + "','" + str(raise_request_id) + "')")
    conn.commit()
    cursor.execute("insert into donations(sender,receiver,amount,donation_type,date,raise_request_id) values('Administrator', 'Hospital', '" + str(amount) + "', 'Cause', now(),'" + str(raise_request_id) + "')")
    conn.commit()
    if remaining_amount == 0:
        cursor.execute("update raise_request set status ='" + str(status_amount_donated) + "' where raise_request_id='" + str(raise_request_id) + "'")
    return render_template("msg.html", message="Amount Donated Successfully", color="bg-success text-white")


@app.route("/viewFundAmount")
def viewFundAmount():
    cursor.execute("select * from bankAccount")
    bankAccounts = cursor.fetchall()
    return render_template("viewFundAmount.html", bankAccounts=bankAccounts)


def get_donor_id(donor_id):
    cursor.execute("select * from donor where donor_id= '" + str(donor_id) + "'")
    donor = cursor.fetchall()
    return donor[0]


@app.route("/donationTransactions")
def donationTransactions():
    if session['role'] == "Admin":
        cursor.execute("select * from donations")
    elif session['role'] == "Hospital":
        cursor.execute("select * from donations where raise_request_id in (select raise_request_id from raise_request where hospital_id = '"+ str(session['hospital_id']) +"' and receiver= 'Hospital'order by donations_id desc )")

    elif session['role'] == "Donor":
        cursor.execute("select * from donations where donor_id = '" + str(session['donor_id']) + "'")
    donations = cursor.fetchall()
    return render_template("donationTransactions.html", donations=donations, get_donor_id=get_donor_id)


@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")


app.run(debug=True)
