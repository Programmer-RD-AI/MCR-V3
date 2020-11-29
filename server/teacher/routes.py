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


@app.route("/Teacher/CRD/Notices")
@app.route("/Teacher/CRD/Notices/")
def crd_notices_teacher():
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
            return render_template("/teacher/cr_notices.html")
        return abort(404)
    except:
        return abort(505)