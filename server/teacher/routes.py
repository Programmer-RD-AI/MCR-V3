from server import *


@app.route("/Teacher")
@app.route("/Teacher/")
def teacher():
    try:
        conditions = [
            "Auth" in session,
            "User Name" in session,
            "Password or Email" in session,
            "Role" in session,
            "Returned Data" in session,
            session["Role"] == "Teacher",
        ]
        if all(conditions):
            return render_template("/teacher/home.html")
        return abort(404)
    except:
        return abort(505)
