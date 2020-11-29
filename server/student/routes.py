from server import *
from server.db.admin.crud_subjects import *
from server.db.admin.crud_users import *


@app.route("/Student")
@app.route("/Student/")
def student_home():
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
        session["Role"] == "Student",
    ]
    if all(conditions):
        subjects = Subjects(subject="")
        results = subjects.get_collections()
        return render_template("/student/home.html", results=results)
    return abort(404)


@app.route("/Student/Log/Out")
@app.route("/Student/Log/Out/")
def log_out_student():
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
        session["Role"] == "Student",
    ]
    if all(conditions):
        session.pop("Auth", None)
        session.pop("User Name", None)
        session.pop("Password or Email", None)
        session.pop("Role", None)
        session.pop("Returned Data", None)
        return redirect("/")
    return abort(404)
# http://192.168.1.9:5623/Student/Class/A
@app.route('/Student/Class/<string:class_name>')
def get_class_info(class_name):
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
        session["Role"] == "Student",
    ]
    if all(conditions):
        pass
    return abort(404)