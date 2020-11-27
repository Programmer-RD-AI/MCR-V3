from server import *
from server.db.admin.crud_users import *


@app.route("/Admin/")
@app.route("/Admin")
def admin_home():
    try:
        conditions = [
            "Auth" in session,
            "User Name" in session,
            "Password or Email" in session,
            "Role" in session,
            "Returned Data" in session,
            session["Role"] == "Admin",
        ]
        if all(conditions):
            return render_template("/admin/home.html")
        return abort(404)
    except:
        return abort(505)


@app.route("/Admin/CRUD/Teacher")
@app.route("/Admin/CRUD/Teacher/")
@app.route("/Admin/CRUD/Teachers")
@app.route("/Admin/CRUD/Teachers/")
def admin_crud_teacher():
    try:
        conditions = [
            "Auth" in session,
            "User Name" in session,
            "Password or Email" in session,
            "Role" in session,
            session["Role"] == "Admin",
            "Returned Data" in session,
        ]
        if all(conditions):
            if request.method == "POST":
                user_name = request.form["UN"]
                password = request.form["P"]
                email = request.form["E"]
                subject = request.form['S']
                t = Teacher()
                result = t.add_teacher(user_name=user_name,password=password,email=email,subject=subject)
                print(result)
                flash(result,'success')
            else:
                return render_template("/admin/crud.html", type_of_crud_user="Teacher")
        return abort(404)
    except:
        return abort(505)


@app.route("/Admin/CRUD/Student")
@app.route("/Admin/CRUD/Student/")
@app.route("/Admin/CRUD/Students")
@app.route("/Admin/CRUD/Students/")
def admin_crud_student():
    pass
