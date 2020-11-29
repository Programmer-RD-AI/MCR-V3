from server import *
import random
from server.db.home.autentication import Sign_In


@app.route("/")
def home():
    try:
        links = [
            "https://1.bp.blogspot.com/-3Z4UgmzETpw/WS59lSXgWXI/AAAAAAAAAEk/QfHUxwXEPeE9Bo2Nu4yBKcn5VrGFn-D2wCLcB/s1600/Hello.gif",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSp5z7ZISKeWBfOnIiuAExY78oIlUXX-Hfqgw&usqp=CAU",
            "https://i.pinimg.com/originals/4d/7a/8f/4d7a8f9b9cd725332996654512169a50.gif",
        ]
        gif_link = random.choice(links)
        return render_template("/home/home.html", img=gif_link)
    except:
        return abort(505)


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
                session["Returned Data"] = result
                return redirect("/" + role + "/")
            else:
                flash(
                    "Inccorrect pair of user name and password and user name and email or wrong role please check again !",
                    "danger",
                )
            return redirect("/")
        else:
            return render_template('/home/sign_in.html')