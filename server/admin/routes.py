from server import *
from server.db.admin.crud_users import *
from server.db.admin.crud_subjects import *


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
                subject = request.form["S"]
                t = Teacher()
                result = t.add_teacher(
                    user_name=user_name, password=password, email=email, subject=subject
                )
                print(result)
                flash(result, "success")
                return redirect("/Admin")
            else:
                subjects = Subjects(subject="")
                results = subjects.get_collections()
                return render_template(
                    "/admin/crud_users.html",
                    type_of_crud_user="Teacher",
                    subjects=results,
                )
        return abort(404)
    except:
        return abort(505)


@app.route("/Admin/CRUD/Teacher/Delete/<string:user_name>/<string:email>")
@app.route("/Admin/CRUD/Teacher/Delete/<string:user_name>/<string:email>/")
@app.route("/Admin/CRUD/Teachers/Delete/<string:user_name>/<string:email>/")
@app.route("/Admin/CRUD/Teachers/Delete/<string:user_name>/<string:email>")
def admin_crud_teacher(user_name, email):
    try:
        user_name = json.load(user_name)
        email = json.load(email)
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
                t = Teacher(user_name="", password="", email="")
                result = t.delete_teacher(email=email, user_name=user_name)
                if result:
                    flash("Successfully deleted the teacher.", "success")
                    return redirect("/Admin/")
                flash("AN error occurred ! ", "danger")
                return redirect(
                    "/Admin/CRUD/Teacher/Delete/"
                    + json.dump(user_name)
                    + "/"
                    + json.dump(email)
                )
            else:
                return render_template(
                    "/admin/d_users.html",
                    type_of_crud_user="Teacher",
                )
        return abort(404)
    except:
        return abort(505)


@app.route("/Admin/CRUD/Teacher/Update/<string:user_name>/<string:email>")
@app.route("/Admin/CRUD/Teacher/Update/<string:user_name>/<string:email>/")
@app.route("/Admin/CRUD/Teachers/Update/<string:user_name>/<string:email>/")
@app.route("/Admin/CRUD/Teachers/Update/<string:user_name>/<string:email>")
def admin_crud_teacher(user_name, email):
    try:
        user_name = json.load(user_name)
        email = json.load(email)
        t = Teacher(user_name="", password="", email="")
        result = t.get_data_of_teacher()
        if result[0] is False:
            return abort(404)
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
                new_user_name = request.form["UN"]
                new_password = request.form["P"]
                new_email = request.form["E"]
                new_subject = request.form["S"]
                new_role = request.form["R"]
                result = t.update_teacher(
                    new_info={
                        "User Name": new_user_name,
                        "Password": new_password,
                        "Email": new_email,
                        "Role": new_role,
                        "Subject": new_subject,
                    },
                    old_info=result[1][0],
                )
                if result:
                    flash("Teacher info updated ! ", "success")
                    return redirect("/Admin/")
                flash("An error Occured ! ", "danger")
                return redirect("/Admin/")
            else:
                return render_template(
                    "/admin/u_users.html",
                    type_of_crud_user="Teacher",
                )
        return abort(404)
    except:
        return abort(505)


@app.route("/Admin/CRUD/Student")
@app.route("/Admin/CRUD/Student/")
@app.route("/Admin/CRUD/Students")
@app.route("/Admin/CRUD/Students/")
def admin_crud_student():
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
                s = Students()
                result = s.add_student(
                    user_name=user_name, password=password, email=email
                )
                print(result)
                flash(result, "success")
                return redirect("/Admin")
            else:
                return render_template(
                    "/admin/crud_users.html", type_of_crud_user="Student"
                )
        return abort(404)
    except:
        return abort(505)


@app.route("/Admin/CRUD/Student/Update/<string:user_name>/<string:email>")
@app.route("/Admin/CRUD/Student/Update/<string:user_name>/<string:email>/")
@app.route("/Admin/CRUD/Students/Update/<string:user_name>/<string:email>")
@app.route("/Admin/CRUD/Students/Update/<string:user_name>/<string:email>/")
def admin_crud_student():
    try:
        user_name = json.load(user_name)
        
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
                s = Students()
                result = s.add_student(
                    user_name=user_name, password=password, email=email
                )
                print(result)
                flash(result, "success")
                return redirect("/Admin")
            else:
                return render_template(
                    "/admin/crud_users.html", type_of_crud_user="Student"
                )
        return abort(404)
    except:
        return abort(505)


@app.route("/Admin/CRUD/Subjects")
@app.route("/Admin/CRUD/Subjects/")
@app.route("/Admin/CRUD/Subject")
@app.route("/Admin/CRUD/Subjects/")
def admin_crud_subjects():
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
                subject = request.form["S"]
                s = Subjects(subject=subject)
                result = s.add_collection()
                if result:
                    flash("New Subject Created ! ", "success")
                    return redirect("/Admin/CRUD/Subjects")
                flash(
                    "An Error Occurred or there another subject with the exact sam subject name.",
                    "danger",
                )
                return redirect("/Admin/CRUD/Subjects")
            else:
                return render_template("/admin/crud_subjects.html")
        return abort(404)
    except:
        return abort(505)


@app.route("/Admin/CRUD/Subjects/Update/<string:subject_name>")
@app.route("/Admin/CRUD/Subjects/Update/<string:subject_name>/")
@app.route("/Admin/CRUD/Subject/Update/<string:subject_name>")
@app.route("/Admin/CRUD/Subjects/Update/<string:subject_name>/")
def admin_crud_subjects_update(subject_name):
    try:
        subject_name = json.load(subject_name)
        conditions = [
            "Auth" in session,
            "User Name" in session,
            "Password or Email" in session,
            "Role" in session,
            session["Role"] == "Admin",
            "Returned Data" in session,
        ]
        if all(conditions):
            s = Subjects(subject=subject_name)
            result = s.check_if_exits()
            if not result:
                return abort(404)
            if request.method == "POST":
                subject = request.form["S"]
                s = Subjects(subject=subject)
                result = s.update_collection(subject_name)
                if result:
                    flash("Updated ! ", "success")
                    return redirect("/Admin/CRUD/Subjects/Update/" + subject)
                flash("An error occurred ! ", "danger")
                return redirect("/Admin/CRUD/Subjects/Update/" + subject_name)
            else:
                return render_template("/admin/u_subjects.html", old_name=subject_name)
        return abort(404)
    except:
        return abort(505)


@app.route("/Admin/CRUD/Subjects/Delete/<string:subject_name>")
@app.route("/Admin/CRUD/Subjects/Delete/<string:subject_name>/")
@app.route("/Admin/CRUD/Subject/Delete/<string:subject_name>")
@app.route("/Admin/CRUD/Subjects/Delete/<string:subject_name>/")
def admin_crud_subjects_delete(subject_name):
    try:
        subject_name = json.load(subject_name)
        conditions = [
            "Auth" in session,
            "User Name" in session,
            "Password or Email" in session,
            "Role" in session,
            session["Role"] == "Admin",
            "Returned Data" in session,
        ]
        if all(conditions):
            s = Subjects(subject=subject_name)
            result = s.check_if_exits()
            if not result:
                return abort(404)
            if request.method == "POST":
                s = Subjects(subject=subject_name)
                result = s.delete_collection()
                if result:
                    flash("Deleted ! ", "success")
                    return redirect("/Admin/CRUD/Subjects/")
                flash("An error occurred ! ", "danger")
                return redirect("/Admin/CRUD/Subjects")
            else:
                return render_template("/admin/d_subjects.html", name=subject_name)
        return abort(404)
    except:
        return abort(505)
