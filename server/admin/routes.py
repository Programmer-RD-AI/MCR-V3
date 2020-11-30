from server import *
from server.db.admin.crud_users import *
from server.db.admin.crud_subjects import *
from server.db.notices import *
from server import session
import base64


@app.route("/Admin/")
@app.route("/Admin")
def admin_home():
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    if all(conditions):
        if session["Role"] == "Admin":
            return render_template("/admin/home.html")
    return abort(404)


@app.route("/Admin/Log/Out")
@app.route("/Admin/Log/Out/")
def log_out():
    try:
        pop = ["Auth", "User Name", "Password", "Role", "Returned Data"]
        for poper in pop:
            session.pop(poper, None)
        return redirect("/")
    except:
        return abort(505)


@app.route("/Admin/CRUD/Teacher", methods=["POST", "GET"])
@app.route("/Admin/CRUD/Teacher/", methods=["POST", "GET"])
@app.route("/Admin/CRUD/Teachers", methods=["POST", "GET"])
@app.route("/Admin/CRUD/Teachers/", methods=["POST", "GET"])
def admin_crud_teacher():
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
            if subject == "None":
                flash("Please seleect a subject !", "danger")
                return redirect("/Admin/CRUD/Teacher")
            if subject == "Choose Subject":
                flash("Please select a subject ! ", "danger")
                return redirect("/Admin/CRUD/Teacher")
            t = Teacher(
                user_name=user_name, password=password, email=email, subject=subject
            )
            result = t.add_teacher()
            print(result)
            if result[0] is True:
                flash(result[1], "success")
            else:
                flash(result[1], "danger")
            return redirect("/Admin/CRUD/Teacher")
        else:
            subjects = Subjects(subject="A")
            results = subjects.get_collections()
            t = Teacher(user_name="A", password="A", email="A", subject="A")
            final_results = []
            lenght_to_go = t.get_all_teachers()
            for info in lenght_to_go[0]:
                get_teachers_result = info
                get_teachers_result_ = {}
                get_teachers_result_["User Name"] = encode_data(
                    get_teachers_result["User Name"]
                )
                get_teachers_result_["Email"] = encode_data(
                    get_teachers_result["Email"]
                )
                final_results.append([get_teachers_result, get_teachers_result_])
            print(final_results)
            try:
                return render_template(
                    "/admin/crud_teacher.html", subjects=results, teachers=final_results
                )
            except:
                return render_template(
                    "/admin/crud_teacher.html", subjects=results, teachers=[]
                )
    return abort(404)


@app.route(
    "/Admin/CRUD/Teacher/Delete/<string:user_name>/<string:email>",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRUD/Teacher/Delete/<string:user_name>/<string:email>/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRUD/Teachers/Delete/<string:user_name>/<string:email>/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRUD/Teachers/Delete/<string:user_name>/<string:email>",
    methods=["POST", "GET"],
)
def admin_crud_delete_teacher(user_name, email):
    user_name = decode_data(user_name)
    email = decode_data(email)
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
            t = Teacher(user_name="", password="", email="", subject="")
            result = t.delete_teacher(email=email, user_name=user_name)
            if result is True:
                flash("Successfully deleted the teacher.", "success")
                return redirect(
                    "/Admin/CRUD/Teacher/Delete/"
                    + encode_data(message=user_name)
                    + "/"
                    + encode_data(message=email)
                )
            flash("AN error occurred ! ", "danger")
            return redirect(
                "/Admin/CRUD/Teacher/Delete/"
                + encode_data(message=user_name)
                + "/"
                + encode_data(message=email)
            )
        else:
            t = Teacher(
                user_name=user_name, password="password", subject="gregt", email=email
            )
            result = t.get_data_of_teacher(user_name=user_name, email=email)
            return render_template("/admin/d_teacher.html", info=result[1])
    return abort(404)


@app.route(
    "/Admin/CRUD/Teacher/Update/<string:user_name>/<string:email>",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRUD/Teacher/Update/<string:user_name>/<string:email>/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRUD/Teachers/Update/<string:user_name>/<string:email>/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRUD/Teachers/Update/<string:user_name>/<string:email>",
    methods=["POST", "GET"],
)
def admin_crud_update_teacher(user_name, email):
    user_name = decode_data(user_name)
    email = decode_data(email)
    t = Teacher(user_name="", password="", email="", subject="")
    result = t.get_data_of_teacher(user_name=user_name, email=email)
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
            if new_role == "Student" or new_subject == "None":
                if new_role != "Student":
                    flash("Please select the role as Student", "danger")
                    return redirect("/Admin/CRUD/Teacher")
                if new_subject != "None":
                    flash("Please select the subject as None ! ", "danger")
                    return redirect("/Admin/CRUD/Teacher")
                print(result)
                result_ = t.update_teacher(
                    new_info={
                        "User Name": new_user_name,
                        "Password": new_password,
                        "Email": new_email,
                        "Role": new_role,
                    },
                    old_info=result[1][0],
                )
                print(result_)
                if result_ is False:
                    flash(
                        "There is another user with the same info or an error occured !",
                        "danger",
                    )
                return redirect("/Admin/CRUD/Teacher")
            else:
                result = t.update_teacher(
                    new_info={
                        "User Name": new_user_name,
                        "Password": new_password,
                        "Email": new_email,
                        "Role": new_role,
                        "Subject": new_subject,
                    },
                    old_info=result[1],
                )
                print(result)
                if result is False:
                    flash(
                        "There is another user with the same info or an error occured !",
                        "danger",
                    )
                return redirect("/Admin/CRUD/Teacher")
            if result is True:
                flash("Teacher info updated ! ", "success")
                return redirect("/Admin/CRUD/Teacher")
            if result is False:
                flash(result, "danger")
                return redirect("/Admin/CRUD/Teacher")
        else:
            s = Subjects(subject="")
            result = s.get_collections()
            t = Teacher(
                user_name=user_name, password="password", email="go2ranuga", subject=""
            )
            info = t.get_data_of_teacher(user_name=user_name, email=email)
            print(info)
            return render_template(
                "/admin/u_teacher.html",
                subjects=result,
                email=info[1][0]["Email"],
                password=info[1][0]["Password"],
                user_name=info[1][0]["User Name"],
            )
    return abort(404)


@app.route("/Admin/CRUD/Student", methods=["POST", "GET"])
@app.route("/Admin/CRUD/Student/", methods=["POST", "GET"])
@app.route("/Admin/CRUD/Students", methods=["POST", "GET"])
@app.route("/Admin/CRUD/Students/", methods=["POST", "GET"])
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
                s = Students(user_name=user_name, password=password, email=email)
                result = s.add_student()
                if result[0] is True:
                    flash(result[1], "success")
                else:
                    flash(result[1], "danger")
                return redirect("/Admin/CRUD/Student")
            else:
                s = Students(user_name="", password="", email="")
                results = s.get_students()
                final = []
                for result in results[1]:
                    result_not_encoded = result
                    result_encoded = {}
                    result_encoded["User Name"] = encode_data(
                        result_not_encoded["User Name"]
                    )
                    result_encoded["Password"] = encode_data(
                        result_not_encoded["Password"]
                    )
                    result_encoded["Email"] = encode_data(result_not_encoded["Email"])
                    del result_not_encoded["_id"]
                    print([result_not_encoded, result_encoded])
                    final.append([result_not_encoded, result_encoded])
                print(final)
                return render_template("/admin/crud_student.html", students=final)
        return abort(404)
    except:
        return abort(505)


@app.route(
    "/Admin/CRUD/Student/Update/<string:user_name>/<string:email>",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRUD/Student/Update/<string:user_name>/<string:email>/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRUD/Students/Updates/<string:user_name>/<string:email>",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRUD/Students/Updates/<string:user_name>/<string:email>/",
    methods=["POST", "GET"],
)
def admin_crud_update_student(user_name, email):
    user_name = decode_data(user_name)
    email = decode_data(email)
    s = Students(user_name=user_name, password=email + user_name, email=email)
    old_info = s.get_data_of_student(user_name=user_name, email=email)
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
            new_role = request.form["R"]
            new_subject = request.form["S"]
            if new_role == "None":
                flash("Please select a role ! ", "danger")
                return redirect(
                    "/Admin/CRUD/Student/Update/"
                    + encode_data(user_name)
                    + "/"
                    + encode_data(email)
                )
            if new_subject != "None" or new_role == "Teacher":
                if new_role != "Teacher":
                    flash(
                        "Please select teacher as the role if you want to make this student a teacher",
                        "danger",
                    )
                    return redirect(
                        "/Admin/CRUD/Student/Update/"
                        + encode_data(user_name)
                        + "/"
                        + encode_data(email)
                    )
                if new_subject == "None":
                    flash("Please select a subject as a teacher ! ", "danger")
                    return redirect(
                        "/Admin/CRUD/Student/Update/"
                        + encode_data(user_name)
                        + "/"
                        + encode_data(email)
                    )
                result_update_student = s.update_student(
                    new_info={
                        "User Name": new_user_name,
                        "Password": new_password,
                        "Email": new_email,
                        "Role": new_role,
                        "Subject": new_subject,
                    },
                    old_info=old_info[1],
                )
                if result_update_student is False:
                    flash(
                        "There is another user with the same info or an error occured ! ",
                        "danger",
                    )
                    return redirect("/Admin/CRUD/Student")
            else:
                result_update_student = s.update_student(
                    new_info={
                        "User Name": new_user_name,
                        "Password": new_password,
                        "Email": new_email,
                        "Role": new_role,
                    },
                    old_info=old_info[1],
                )
                if result_update_student is False:
                    flash(
                        "There is another user with the same info or an error occured ! ",
                        "danger",
                    )
                    return redirect("/Admin/CRUD/Student")

            flash("Updated ! ", "success")
            return redirect("/Admin/CRUD/Student")
        else:
            s = Students(user_name=user_name, password="password", email=email)
            result = s.get_data_of_student(user_name=user_name, email=email)
            subjects = Subjects(subject="grdfg")
            result_subject = subjects.get_collections()
            print(result_subject)
            print(result)
            return render_template(
                "/admin/u_student.html",
                email=result[1][0]["Email"],
                user_name=result[1][0]["User Name"],
                password=result[1][0]["Password"],
                subjects=result_subject,
            )
    return abort(404)


@app.route(
    "/Admin/CRUD/Student/Delete/<string:user_name>/<string:email>",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRUD/Student/Delete/<string:user_name>/<string:email>/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRUD/Students/Deletes/<string:user_name>/<string:email>",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRUD/Students/Deletes/<string:user_name>/<string:email>/",
    methods=["POST", "GET"],
)
def admin_crud_delete_student(user_name, email):
    try:
        user_name = decode_data(user_name)
        email = decode_data(email)
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
                s = Students(user_name=user_name, password="password", email=email)
                result = s.get_data_of_student(user_name=user_name, email=email)
                result_del = s.delete_student(infos=result[1])
                if result_del is False:
                    flash("An Error Occurred ! ", "danger")
                    return redirect(
                        "/Admin/CRUD/Student/Delete/"
                        + encode_data(user_name)
                        + "/"
                        + encode_data(email)
                    )
                flash("Deleted Successfully ! ", "success")
                return redirect("/Admin/CRUD/Student")
            else:
                s = Students(user_name=user_name, password="password", email=email)
                result = s.get_data_of_student(user_name=user_name, email=email)
                print(result)
                return render_template("/admin/d_student.html", info=result[1][0])
        return abort(404)
    except:
        return abort(505)


@app.route("/Admin/CRUD/Subjects", methods=["POST", "GET"])
@app.route("/Admin/CRUD/Subjects/", methods=["POST", "GET"])
@app.route("/Admin/CRUD/Subject", methods=["POST", "GET"])
@app.route("/Admin/CRUD/Subjects/", methods=["POST", "GET"])
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
                sliced_result = subject.split()
                if " " in sliced_result:
                    flash("There cant be any spaces in the subject name !!", "danger")
                    return redirect("/Admin/CRUD/Subject")
                s = Subjects(subject=f"{subject}")
                result = s.add_collection()
                print(result)
                if result:
                    flash("New Subject Created ! ", "success")
                    return redirect("/Admin/CRUD/Subjects")
                flash(
                    "An Error Occurred or there another subject with the exact same subject name.",
                    "danger",
                )
                return redirect("/Admin/CRUD/Subjects")
            else:
                subjects = Subjects(subject="A")
                results = subjects.get_collections()
                json_encoded = []
                final = []
                for result in results:
                    result = str(result)
                    base64_message = encode_data(result)
                    json_encoded.append(base64_message)
                print(json_encoded)
                for subject, subject_encoded in zip(results, json_encoded):
                    final.append([subject, subject_encoded])
                return render_template("/admin/crud_subjects.html", final=final)
        return abort(404)
    except:
        return abort(505)


@app.route("/Admin/CRUD/Subjects/Update/<string:subject_name>", methods=["POST", "GET"])
@app.route(
    "/Admin/CRUD/Subjects/Update/<string:subject_name>/", methods=["POST", "GET"]
)
@app.route("/Admin/CRUD/Subject/Update/<string:subject_name>", methods=["POST", "GET"])
@app.route(
    "/Admin/CRUD/Subjects/Update/<string:subject_name>/", methods=["POST", "GET"]
)
def admin_crud_subjects_update(subject_name):
    old_subject_name = subject_name
    try:
        subject_name = decode_data(str(subject_name))
    except:
        subject_name = subject_name
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
            sliced_result = subject.strip()
            if " " in sliced_result:
                flash("There cant be any spaces in the subject name !!!", "dange")
                return redirect("/Admin/CRUD/Subject/Update/" + old_subject_name)
            s = Subjects(subject=subject)
            exists_result = s.check_if_exits()
            if exists_result is True:
                flash(
                    "There is another subject with the same name please try again later ! or you didn't change the subject name",
                    "danger",
                )
                return redirect("/Admin/CRUD/Subjects/Update/" + old_subject_name)
            result = s.update_collection(subject_name)
            if result:
                flash("Updated ! ", "success")
                return redirect("/Admin/CRUD/Subjects")
            flash("An error occurred ! ", "danger")
            return redirect("/Admin/CRUD/Subjects/Update/" + old_subject_name)
        else:
            return render_template("/admin/u_subjects.html", old_name=subject_name)
    return abort(404)


@app.route("/Admin/CRUD/Subjects/Delete/<string:subject_name>", methods=["POST", "GET"])
@app.route(
    "/Admin/CRUD/Subjects/Delete/<string:subject_name>/", methods=["POST", "GET"]
)
@app.route("/Admin/CRUD/Subject/Delete/<string:subject_name>", methods=["POST", "GET"])
@app.route(
    "/Admin/CRUD/Subjects/Delete/<string:subject_name>/", methods=["POST", "GET"]
)
def admin_crud_subjects_delete(subject_name):
    old_subject_name = subject_name
    subject_name = decode_data(subject_name)
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
        print(result)
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


def decode_data(message):
    base64_bytes = message.encode("ascii")
    subject_name = base64.b64decode(base64_bytes).decode("ascii")
    return subject_name


def encode_data(message):
    message_bytes = message.encode("ascii")
    base64_message = base64.b64encode(message_bytes).decode("ascii")
    return base64_message


@app.route("/Admin/CRD/Notices", methods=["POST", "GET"])
@app.route("/Admin/CRD/Notices/", methods=["POST", "GET"])
@app.route("/Admin/CRD/Notice", methods=["POST", "GET"])
@app.route("/Admin/CRD/Notice/", methods=["POST", "GET"])
def crd_notices():
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
            title = request.form["T"]
            description = request.form["D"]
            result = add_notice(title=title, description=description)
            if result is True:
                flash("New Notice added ! ", "success")
                return redirect("/Admin/CRD/Notices")
            flash("An error occured ! ", "danger")
            return redirect("/Admin/CRD/Notices")
        else:
            notices = get_notices()
            return render_template("/admin/crd_notices.html", notices=notices)
    return abort(404)


@app.route(
    "/Admin/CRD/Notices/Delete/<string:title>/<string:description>",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRD/Notices/Delete/<string:title>/<string:description>/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRD/Notice/Delete/<string:title>/<string:description>",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/CRD/Notice/Delete/<string:title>/<string:description>/",
    methods=["POST", "GET"],
)
def crd_notices_delete(title, description):
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    if all(conditions):
        if session["Role"] == "Admin":
            if request.method == "POST":
                result = delete_notice(title=title, description=description)
                if result is True:
                    flash("Deleted Notice ! ", "success")
                    return redirect("/Admin/CRD/Notices")
                else:
                    flash("An error occured ! ", "danger")
                    return redirect(f"/Admin/CRD/Notices/Delete/{title}/{description}")
            else:
                return render_template("/admin/d_notice.html", title=title)
        return abort(404)
    return abort(404)
