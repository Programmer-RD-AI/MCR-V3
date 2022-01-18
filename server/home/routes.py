from server import *
from server.db.home.autentication import Register, Sign_In


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        whatsapp_number = request.form["WAN"]
        user_name = request.form["UN"]
        password = request.form["P"]
        email = request.form["E"]
        if str(whatsapp_number)[0] != "9":
            flash("Please enter a number as like 94778899111", "danger")
            return redirect("/")
        whatsapp_number = int(whatsapp_number)
        r = Register(user_name, password, whatsapp_number, email)
        results = r.check()
        if results[0] is True:
            flash(results[1][0], "success")
        else:
            for result in results[1]:
                flash(result, "danger")
        return redirect("/")
    else:
        return render_template("/home/home.html")


@app.route("/Sign/In", methods=["POST", "GET"])
@app.route("/Sign/In/", methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        user_name = request.form["UN"]
        password_or_email = request.form["PE"]
        role = request.form["R"]
        if role == "Choose":
            flash(
                "please select the role !!!!!!!!!!!!",
                "danger",
            )
            return redirect("/Sign/In")
        si = Sign_In(user_name=user_name,
                     password_or_email=password_or_email,
                     role=role)
        result = si.check()
        if result[0]:
            session["Auth"] = True
            session["User Name"] = user_name
            session["Password or Email"] = password_or_email
            session["Role"] = role
            session["Returned Data"] = result
            return redirect("/" + role + "/")
        else:
            flash(
                "Inccorrect pair of user name and password and user name and email or wrong role please check again !",
                "danger",
            )
        return redirect("/")
    else:
        return render_template("/home/sign_in.html")
