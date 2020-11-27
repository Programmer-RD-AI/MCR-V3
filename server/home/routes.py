from server import *
import random
from server.db.home.autentication import Sign_In


@app.route("/")
def home():
    links = [
        "https://media0.giphy.com/media/SSirUu2TrV65ymCi4J/giphy.gif",
        "https://media0.giphy.com/media/ZXlczQhl0lQLaUIzCu/giphy.gif",
        "https://media1.tenor.com/images/a4b85afdffa6b8f0f798f363ba7fc086/tenor.gif?itemid=4458331",
    ]
    gif_link = random.choice(links)
    return render_template("/home/home.html", img=gif_link)


@app.route("/Sign/In", methods=["POST", "GET"])
@app.route("/Sign/In/", methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        user_name = request.form["UN"]
        password_or_email = request.form["PE"]
        role = request.form["R"]
        if role == "Choose":
            flash(
                "No god no !!! please select the role you dumb person !!!!!!!!!!!!",
                "danger",
            )
            return redirect("/Sign/In")
        si = Sign_In(
            user_name=user_name, password_or_email=password_or_email, role=role
        )
        result = si.check()
        if result[0]:
            session["Auth"] = True
            session["User Name"] = user_name
            session["Password or Email"] = password_or_email
            session["Role"] = role
            session['Returned Data'] = result
            return redirect("/" + role + "/")
        else:
            flash(
                "Inccorrect pair of user name and password and user name and email or wrong role please check again !",
                "danger",
            )
        return redirect("/")
    else:
        return render_template("/home/sign_in.html")
