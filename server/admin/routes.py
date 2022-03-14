import base64
import pickle

import matplotlib.pyplot as plt
import numpy as np

from mongodb.get_the_last_id import *
from server import *
from server import session
from server.db.admin.crud_subjects import *
from server.db.admin.crud_users import *
from server.db.admin.files import File_Admin
from server.db.admin.sms import SMS
from server.db.admin.stream import *
from server.db.home.autentication import *
from server.db.notices import *


def get_balance():
    balance = SMS(phone_numbers=[], message="")
    balance = balance.get_balance()
    return balance


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
            return render_template("/admin/home.html",
                                   sms_balance=get_balance(),
                                   page="Home")
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
            whatsapp_number = request.form["WAN"]
            if subject == "None":
                flash("Please seleect a subject !", "danger")
                return redirect("/Admin/CRUD/Teacher")
            if subject == "Choose Subject":
                flash("Please select a subject ! ", "danger")
                return redirect("/Admin/CRUD/Teacher")
            t = Teacher(
                user_name=user_name,
                password=password,
                email=email,
                subject=subject,
                whatsapp_number=whatsapp_number,
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
            t = Teacher(user_name="A",
                        password="A",
                        email="A",
                        subject="A",
                        whatsapp_number=0)
            final_results = []
            lenght_to_go = t.get_all_teachers()
            for info in lenght_to_go[0]:
                get_teachers_result = info
                get_teachers_result_ = {}
                get_teachers_result_["User Name"] = encode_data(
                    get_teachers_result["User Name"])
                get_teachers_result_["Email"] = encode_data(
                    get_teachers_result["Email"])
                final_results.append(
                    [get_teachers_result, get_teachers_result_])
            print(final_results)
            try:
                return render_template(
                    "/admin/crud_teacher.html",
                    sms_balance=get_balance(),
                    subjects=results,
                    teachers=final_results,
                    page="Teachers",
                )
            except:
                return render_template(
                    "/admin/crud_teacher.html",
                    subjects=results,
                    sms_balance=get_balance(),
                    teachers=[],
                    page="Teachers",
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
            t = Teacher(user_name="",
                        password="",
                        email="",
                        subject="",
                        whatsapp_number="")
            result = t.delete_teacher(email=email, user_name=user_name)
            if result is True:
                flash("Successfully deleted the teacher.", "success")
                return redirect("/Admin/CRUD/Teacher/Delete/" +
                                encode_data(message=user_name) + "/" +
                                encode_data(message=email))
            flash("AN error occurred ! ", "danger")
            return redirect("/Admin/CRUD/Teacher/Delete/" +
                            encode_data(message=user_name) + "/" +
                            encode_data(message=email))
        else:
            t = Teacher(
                user_name=user_name,
                password="password",
                subject="gregt",
                email=email,
                whatsapp_number="",
            )
            result = t.get_data_of_teacher(user_name=user_name, email=email)
            print("+" * 100)
            try:
                return render_template(
                    "/admin/d_teacher.html",
                    sms_balance=get_balance(),
                    info=result[1][0],
                    page="Teachers",
                )
            except:
                flash(f"Successfuly delted User !", "success")
                return redirect("/Admin")
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
    t = Teacher(user_name="",
                password="",
                email="",
                subject="",
                whatsapp_number="")
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
            new_whatsapp_number = request.form["WAN"]
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
                        "Whatapp Number": new_whatsapp_number,
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
                        "Whatapp Number": new_whatsapp_number,
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
                user_name=user_name,
                password="password",
                email="go2ranuga",
                subject="",
                whatsapp_number="",
            )
            info = t.get_data_of_teacher(user_name=user_name, email=email)
            print(info)
            return render_template(
                "/admin/u_teacher.html",
                sms_balance=get_balance(),
                subjects=result,
                email=info[1][0]["Email"],
                password=info[1][0]["Password"],
                user_name=info[1][0]["User Name"],
                whatsapp_number=info[1][0]["Whatsapp Number"],
                page="Teachers",
            )
    return abort(404)


@app.route("/Admin/CRUD/Student", methods=["POST", "GET"])
@app.route("/Admin/CRUD/Student/", methods=["POST", "GET"])
@app.route("/Admin/CRUD/Students", methods=["POST", "GET"])
@app.route("/Admin/CRUD/Students/", methods=["POST", "GET"])
def admin_crud_student():
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
            whatsapp_number = request.form["WAN"]
            s = Students(
                user_name=user_name,
                password=password,
                email=email,
                whatsapp_number=whatsapp_number,
            )
            result = s.add_student()
            if result[0] is True:
                flash(result[1], "success")
            else:
                flash(result[1], "danger")
            return redirect("/Admin/CRUD/Student")
        else:
            s = Students(user_name="",
                         password="",
                         email="",
                         whatsapp_number="")
            results = s.get_students()
            final = []
            for result in results[1]:
                result_not_encoded = result
                result_encoded = {}
                result_encoded["User Name"] = encode_data(
                    result_not_encoded["User Name"])
                result_encoded["Password"] = encode_data(
                    result_not_encoded["Password"])
                result_encoded["Email"] = encode_data(
                    result_not_encoded["Email"])
                print(result_not_encoded)
                del result_not_encoded["_id"]
                print([result_not_encoded, result_encoded])
                final.append([result_not_encoded, result_encoded])
            print(final)
            return render_template(
                "/admin/crud_student.html",
                page="Students",
                students=final,
                sms_balance=get_balance(),
            )
    return abort(404)


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
    s = Students(user_name=user_name,
                 password=email + user_name,
                 email=email,
                 whatsapp_number="")
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
            new_whatsapp_number = request.form["WAN"]
            if new_role == "None":
                flash("Please select a role ! ", "danger")
                return redirect("/Admin/CRUD/Student/Update/" +
                                encode_data(user_name) + "/" +
                                encode_data(email))
            if new_subject != "None" or new_role == "Teacher":
                if new_role != "Teacher":
                    flash(
                        "Please select teacher as the role if you want to make this student a teacher",
                        "danger",
                    )
                    return redirect("/Admin/CRUD/Student/Update/" +
                                    encode_data(user_name) + "/" +
                                    encode_data(email))
                if new_subject == "None":
                    flash("Please select a subject as a teacher ! ", "danger")
                    return redirect("/Admin/CRUD/Student/Update/" +
                                    encode_data(user_name) + "/" +
                                    encode_data(email))
                result_update_student = s.update_student(
                    new_info={
                        "User Name": new_user_name,
                        "Password": new_password,
                        "Email": new_email,
                        "Role": new_role,
                        "Subject": new_subject,
                        "Whatsapp Number": request.form["WAN"],
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
                        "Whatsapp Number": request.form["WAN"],
                    },
                    old_info=old_info[1],
                )
                print("*" * 100)
                print(result_update_student)
                print("*" * 100)
                if result_update_student is False:
                    flash(
                        "There is another user with the same info or an error occured ! ",
                        "danger",
                    )
                    return redirect("/Admin/CRUD/Student")

            flash("Updated ! ", "success")
            return redirect("/Admin/CRUD/Student")
        else:
            s = Students(
                user_name=user_name,
                password="password",
                email=email,
                whatsapp_number="",
            )
            result = s.get_data_of_student(user_name=user_name, email=email)
            subjects = Subjects(subject="grdfg")
            result_subject = subjects.get_collections()
            print(result_subject)
            print(result)
            print(result[1][0]["Whatapp Number"])
            return render_template(
                "/admin/u_student.html",
                email=result[1][0]["Email"],
                user_name=result[1][0]["User Name"],
                password=result[1][0]["Password"],
                sms_balance=get_balance(),
                subjects=result_subject,
                whatsapp_number=result[1][0]["Whatapp Number"],
                page="Students",
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
            s = Students(
                user_name=user_name,
                password="password",
                email=email,
                whatsapp_number="",
            )
            result = s.get_data_of_student(user_name=user_name, email=email)
            result_del = s.delete_student(infos=result[1])
            if result_del is False:
                flash("An Error Occurred ! ", "danger")
                return redirect("/Admin/CRUD/Student/Delete/" +
                                encode_data(user_name) + "/" +
                                encode_data(email))
            flash("Deleted Successfully ! ", "success")
            return redirect("/Admin/CRUD/Student")
        else:
            s = Students(
                user_name=user_name,
                password="password",
                email=email,
                whatsapp_number="",
            )
            result = s.get_data_of_student(user_name=user_name, email=email)
            print(result)
            return render_template(
                "/admin/d_student.html",
                page="Students",
                info=result[1][0],
                sms_balance=get_balance(),
            )
    return abort(404)


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
                    flash("There cant be any spaces in the subject name !!",
                          "danger")
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
                return render_template(
                    "/admin/crud_subjects.html",
                    page="Subjects",
                    sms_balance=get_balance(),
                    final=final,
                )
        return abort(404)
    except:
        return abort(505)


@app.route("/Admin/CRUD/Subjects/Update/<string:subject_name>",
           methods=["POST", "GET"])
@app.route("/Admin/CRUD/Subjects/Update/<string:subject_name>/",
           methods=["POST", "GET"])
@app.route("/Admin/CRUD/Subject/Update/<string:subject_name>",
           methods=["POST", "GET"])
@app.route("/Admin/CRUD/Subjects/Update/<string:subject_name>/",
           methods=["POST", "GET"])
def admin_crud_subjects_update(subject_name):
    old_subject_name = subject_name
    try:
        subject_name = decode_data(str(subject_name))
    except:
        pass
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
                flash("There cant be any spaces in the subject name !!!",
                      "dange")
                return redirect("/Admin/CRUD/Subject/Update/" +
                                old_subject_name)
            s = Subjects(subject=subject)
            exists_result = s.check_if_exits()
            if exists_result is True:
                flash(
                    "There is another subject with the same name please try again later ! or you didn't change the subject name",
                    "danger",
                )
                return redirect("/Admin/CRUD/Subjects/Update/" +
                                old_subject_name)
            result = s.update_collection(subject_name)
            if result:
                flash("Updated ! ", "success")
                return redirect("/Admin/CRUD/Subjects")
            flash("An error occurred ! ", "danger")
            return redirect("/Admin/CRUD/Subjects/Update/" + old_subject_name)
        else:
            return render_template(
                "/admin/u_subjects.html",
                sms_balance=get_balance(),
                old_name=subject_name,
                page="Subjects",
            )
    return abort(404)


@app.route("/Admin/CRUD/Subjects/Delete/<string:subject_name>",
           methods=["POST", "GET"])
@app.route("/Admin/CRUD/Subjects/Delete/<string:subject_name>/",
           methods=["POST", "GET"])
@app.route("/Admin/CRUD/Subject/Delete/<string:subject_name>",
           methods=["POST", "GET"])
@app.route("/Admin/CRUD/Subjects/Delete/<string:subject_name>/",
           methods=["POST", "GET"])
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
            return render_template(
                "/admin/d_subjects.html",
                page="Subjects",
                sms_balance=get_balance(),
                name=subject_name,
            )
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
            return render_template(
                "/admin/crd_notices.html",
                page="Notices",
                sms_balance=get_balance(),
                notices=notices,
            )
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
                    return redirect(
                        f"/Admin/CRD/Notices/Delete/{title}/{description}")
            else:
                return render_template(
                    "/admin/d_notice.html",
                    page="Notices",
                    sms_balance=get_balance(),
                    title=title,
                )
        return abort(404)
    return abort(404)


@app.route(
    "/Admin/RDA/Register",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/RDA/Register/",
    methods=["POST", "GET"],
)
def register():
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
                pass
            else:
                r = Register(user_name="",
                             password="",
                             whatsapp_number="",
                             email="")
                results = r.get_all_to_register_users()
                return render_template(
                    "/admin/register.html",
                    page="Register",
                    sms_balance=get_balance(),
                    results=results,
                )
        return abort(404)
    return abort(404)


@app.route(
    "/Admin/RDA/Register/Admit/<_id>",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/RDA/Register/Admit/<_id>/",
    methods=["POST", "GET"],
)
def register_admit(_id):
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    if all(conditions):
        if session["Role"] == "Admin":
            _id = int(_id)
            r = Register(user_name="",
                         password="",
                         whatsapp_number="",
                         email="")
            result = r.delete_user(_id=_id)
            if result[0] is True or result[1] != []:
                print(result)
                s = Students(
                    user_name=result[1][0]["User Name"],
                    password=result[1][0]["Password"],
                    email=result[1][0]["Email"],
                    whatsapp_number=result[1][0]["Whatsapp Number"],
                )
                s.add_student()
                print("OK")
                flash(f"Successfully admitted user with id:{_id}", "success")
                return redirect("/Admin/RDA/Register")
            flash("An error occured.", "danger")
            return redirect("/Admin/RDA/Register")
        print("DEAD")
        print("*" * 100)
        return abort(404)
    print("DEAD")
    print("*" * 100)
    return abort(404)


@app.route(
    "/Admin/RDA/Register/Reject/<_id>",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/RDA/Register/Reject/<_id>/",
    methods=["POST", "GET"],
)
def register_reject(_id):
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    if all(conditions):
        if session["Role"] == "Admin":
            _id = int(_id)
            r = Register(user_name="",
                         password="",
                         whatsapp_number="",
                         email="")
            result = r.get_user_info_from__id(_id=_id)
            if result[0] is True or result[1] != []:
                send_email(
                    "go2ranugad@gmail.com",
                    "RANUGA D 2008",
                    to_email=result[1][0]["Email"],
                    message="You got reject by MyClassRoom-Admin",
                    subject="You got reject by MyClassRoom-Admin try again.",
                )
                r.delete_user(_id)
                print("OK")
                flash(f"Successfully rejected user with id:{_id}", "success")
                return redirect("/Admin/RDA/Register")
            flash("An error occured.", "danger")
            return redirect("/Admin/RDA/Register")
        print("DEAD")
        print("*" * 100)
        return abort(404)
    print("DEAD")
    print("*" * 100)
    return abort(404)


def send_email(email, password, to_email, message, subject):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    send_to_email = to_email
    msg = MIMEMultipart()
    msg["From"] = email
    msg["To"] = send_to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()


@app.route(
    "/Admin/SMS/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/SMS",
    methods=["POST", "GET"],
)
def sms():
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
                message = request.form["m"]
                ticked = request.form.getlist("K")
                if ticked == []:
                    flash("Please select a student.", "danger")
                    return redirect("/Admin/SMS")
                print(ticked)
                s = Students(user_name="",
                             password="",
                             email="",
                             whatsapp_number="")
                students = s.get_students()
                students = students[1]
                ticked_info = []
                for student in students:
                    if student["User Name"] in ticked:
                        ticked_info.append(student["Whatapp Number"])
                sms = SMS(phone_numbers=ticked_info, message=message)
                result = sms.send()
                flash(
                    f"The amount of money spent to send (Message : {message}) {result[1]}",
                    "success",
                )
                return redirect("/Admin/SMS")
            else:
                s = Students(user_name="",
                             password="",
                             email="",
                             whatsapp_number="")
                kids = s.get_students()
                names = []
                for kid in kids[1]:
                    names.append(kid["User Name"])
                kids = names
                print(kids)
                logs = SMS(phone_numbers=[], message=[])
                logs = logs.get_logs()
                return render_template(
                    "/admin/sms.html",
                    sms_balance=get_balance(),
                    page="SMS",
                    logs=logs,
                    kids=kids,
                )
        return abort(404)
    print("DEAD")
    print("*" * 100)
    return abort(404)


@app.route(
    "/Admin/File/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/File",
    methods=["POST", "GET"],
)
def files():
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
                new_file_type = request.form["NFT"]
                fa = File_Admin(file="", description="")
                if new_file_type in fa.get_all_file_types():
                    flash("There is another file type with the same name !",
                          "danger")
                    return redirect("/Admin/File")
                result = fa.add_file_type(new_file_type)

                if result is True:
                    flash("new file type added", "success")
                    return redirect("/Admin/File/")
                else:
                    flash("An error occured", "danger")
                    return redirect("/Admin/File/")
            else:
                fa = File_Admin(file="", description="")
                file_types = fa.get_all_file_types()
                return render_template(
                    "/admin/file.html",
                    page="Files",
                    sms_balance=get_balance(),
                    file_types=file_types,
                )
        return abort(404)
    return abort(404)


@app.route(
    "/Admin/File/<string:file_type>/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/File/<string:file_type>",
    methods=["POST", "GET"],
)
def file_type(file_type):
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    f = File_Admin(file="", description="")
    if file_type not in f.get_all_file_types():
        return abort(404)
    if all(conditions):
        if session["Role"] == "Admin":
            if request.method == "POST":
                file = request.files["F"]
                desc = request.form["D"]
                f = File_Admin(file=file, description=desc)
                result = f.add(file_type_name=file_type, file=file)
                if result is True:
                    flash("Added File.", "success")
                    return redirect(f"/Admin/File/{file_type}")
                else:
                    flash("An error occured ! ", "danger")
                    return redirect(f"/Admin/File/{file_type}")
            else:
                files = f.get_all_files_in_a_file_type(file_type)
                return render_template(
                    "/admin/file_type.html",
                    page="Files",
                    files=files,
                    file_type=file_type,
                )
        return abort(404)
    return abort(404)


@app.route(
    "/Admin/File/<string:file_type>/Delete/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/File/<string:file_type>/Delete",
    methods=["POST", "GET"],
)
def file_type_delete(file_type):
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    f = File_Admin(file="", description="")
    if file_type not in f.get_all_file_types():
        return abort(404)
    if all(conditions):
        if session["Role"] == "Admin":
            f = File_Admin(file="", description="")
            f.delete_file_type(file_type_name=file_type)
            flash(f"{file_type} deleted.", "success")
            return redirect("/Admin/File")
        return abort(404)
    return abort(404)


@app.route(
    "/Admin/File/<string:file_type>/Update/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/File/<string:file_type>/Update",
    methods=["POST", "GET"],
)
def file_type_update(file_type):
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    f = File_Admin(file="", description="")
    if file_type not in f.get_all_file_types():
        return abort(404)
    if all(conditions):
        if session["Role"] == "Admin":
            if request.method == "POST":
                file_type_new = request.form["N"]
                file_type_old = file_type
                if file_type_new == file_type_old:
                    flash(
                        "The new name and the old name are the exact same !!",
                        "danger")
                    return redirect(f"/Admin/File/{file_type}/Update")
                f.update_file_type(old_file_name=file_type_old,
                                   new_file_name=file_type_new)
                flash(
                    f"Updated ! (Old : {file_type_old} | New : {file_type_new})",
                    "success",
                )
                return redirect("/Admin/File/")
            else:
                return render_template("/admin/file_update.html",
                                       page="Files",
                                       file_type=file_type)
        return abort(404)
    return abort(404)


@app.route(
    "/Admin/File/<string:file_type>/<string:filename>/<string:desc>/Download/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/File/<string:file_type>/<string:filename>/<string:desc>/Download",
    methods=["POST", "GET"],
)
def file_type_download(file_type, filename, desc):
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    f = File_Admin(file="", description="")
    if filename not in f.get_all_files(file_type_name=file_type):
        return abort(404)
    print("OK")
    if file_type not in f.get_all_file_types():
        return abort(404)
    if all(conditions):
        if session["Role"] == "Admin":
            f = File_Admin(file="", description=desc)
            result = f.get(
                file_type_name=file_type,
                description=desc,
                filename=filename,
            )
            print("*+" * 100)
            print(result)
            print("*+" * 100)
            return send_from_directory(result[0],
                                       filename=result[1],
                                       as_attachment=True)


@app.route(
    "/Admin/File/<string:file_type>/<string:filename>/<string:desc>/View/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/File/<string:file_type>/<string:filename>/<string:desc>/View",
    methods=["POST", "GET"],
)
def file_type_view(file_type, filename, desc):
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    f = File_Admin(file="", description="")
    if filename not in f.get_all_files(file_type_name=file_type):
        return abort(404)
    print("OK")
    if file_type not in f.get_all_file_types():
        return abort(404)
    if all(conditions):
        if session["Role"] == "Admin":
            f = File_Admin(file="", description=desc)
            result = f.get(
                file_type_name=file_type,
                description=desc,
                filename=filename,
            )
            return send_from_directory(result[0],
                                       filename=result[1],
                                       as_attachment=False)


@app.route(
    "/Admin/File/<string:file_type>/<string:filename>/<string:desc>/Delete/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/File/<string:file_type>/<string:filename>/<string:desc>/Delete",
    methods=["POST", "GET"],
)
def file_type_delete_file(file_type, filename, desc):
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    f = File_Admin(file="", description="")
    if filename not in f.get_all_files(file_type_name=file_type):
        return abort(404)
    if file_type not in f.get_all_file_types():
        return abort(404)
    if all(conditions):
        if session["Role"] == "Admin":
            f = File_Admin(file="", description=desc)
            f.delete(description=desc,
                     filename=filename,
                     file_type_name=file_type)
            flash("File Deleted Successfuly", "success")
            return redirect(f"/Admin/File/{file_type}")
    return abort(404)


@app.route(
    "/Admin/Settings/Sign/In/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Settings/Sign/In",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Setting/Sign/In",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Setting/Sign/In/",
    methods=["POST", "GET"],
)
def setting_admin_sign_in():
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
                user_name = request.form["UN"]
                password_or_email = request.form["POE"]
                si = Sign_In(
                    user_name=user_name,
                    password_or_email=password_or_email,
                    role="Admin",
                )
                result = si.check()
                if result[0] is True:
                    flash("Autenticated Successfully !", "success")
                    session["Settings ?"] = True
                    return redirect("/Admin/Settings")
                else:
                    flash("Autentication failed !", "danger")
                    try:
                        session["Setting Try"] = session["Setting Try"] + 1
                    except:
                        session["Setting Try"] = 0
                    if session["Setting Try"] == 2:
                        flash("You tried 3 time !", "danger")
                        return redirect("/Admin/Log/Out")
                    return redirect("/Admin/Settings/Sign/In")
            else:
                return render_template("/admin/setting_sign_in.html",
                                       page="Settings")


@app.route(
    "/Admin/Settings",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Settings/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Setting",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Setting/",
    methods=["POST", "GET"],
)
def setting_admin():
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    if all(conditions):
        if session["Role"] == "Admin" and session["Settings ?"] is True:
            if request.method == "POST":
                new_user_name = request.form["NUN"]
                new_password = request.form["NP"]
                new_email = request.form["NE"]
                setting_db = cluster["Auth"]
                setting_collection = setting_db["Auth-Sign-In"]
                old_info = ""
                results = []
                for result in setting_collection.find({"Role": "Admin"}):
                    results.append(result)
                old_info = results[0]
                new_info = {}
                _id = get_custom_last_id(db="Auth", collection="Auth-Sign-In")
                new_info["User Name"] = new_user_name
                new_info["Password"] = new_password
                new_info["Email"] = new_email
                new_info["_id"] = _id
                new_info["Role"] = "Admin"
                setting_collection.delete_one(old_info)
                setting_collection.insert_one(new_info)
                flash("Updated", "success")
                session.drop("Setting ?", None)
                return redirect("/Admin/")
            else:
                return render_template("/admin/setting_update.html",
                                       page="Settings")


@app.route(
    "/Admin/Chats",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Chats/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Chat",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Chat/",
    methods=["POST", "GET"],
)
def chat_admin():
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
                message = request.form["M"]
                s = Stream(
                    message=message,
                    user_name=session["User Name"],
                    role=session["Role"],
                )
                s.add()
                return redirect("/Admin/Chat")
            else:
                messages = Stream(message="", user_name="", role="")
                messages = messages.get()
                messages = messages[::-1]
                return render_template(
                    "/admin/chat.html",
                    page="Chat",
                    messages=messages,
                    user_name=session["User Name"],
                )


@app.route(
    "/Admin/Chats/Delete/<string:_id>",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Chats/Delete/<string:_id>",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Chat/Delete/<string:_id>/",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Chat/Delete/<string:_id>",
    methods=["POST", "GET"],
)
def chat_admin_delete(_id):
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    if all(conditions):
        if session["Role"] == "Admin":
            s = Stream(message="", user_name="", role="")
            result = s.delete(_id, session["Role"])
            if result != True:
                return redirect("/Admin/Log/Out")
            flash("Deleted successfuly", "success")
            return redirect("/Admin/Chat/")


@app.route(
    "/Admin/Predicting/Marks/T1",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Predicting/Marks/T1/",
    methods=["POST", "GET"],
)
def predicting_marks_t1():
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
                gender = request.form["Ge"]
                gender_dict = {"Female": 0, "Male": 1}
                gender = gender_dict[gender]
                age = int(request.form["A"])
                family_size = request.form["FS"]
                family_size_dict = {"Less Than 3": 1, "Bigger Than 3": 0}
                mothers_education = request.form["ME"]
                mothers_education_dict = {"None": 0, "Higher Education": 4}
                fathers_education = request.form["FE"]
                fathers_education_dict = {"None": 0, "Higher Education": 4}
                mothers_job = request.form["MJ"]
                mothers_job_dict = {
                    "At Home": 0,
                    "Health": 1,
                    "Other": 2,
                    "Services": 3,
                    "Teachers": 4,
                }
                fathers_job = request.form["FJ"]
                fathers_job_dict = {
                    "Teachers": 0,
                    "Other": 1,
                    "Services": 2,
                    "Health": 3,
                    "At Home": 4,
                }
                guardian = request.form["G"]
                guardian_dict = {"Mother": 0, "Father": 1, "Other": 2}
                study_time = int(request.form["ST"])
                exam_fails = int(request.form["EF"])
                school_support = request.form["SS"]
                school_support_dict = {"Yes": 0, "No": 1}
                family_support = request.form["FSS"]
                family_support_dict = {"No": 0, "Yes": 1}
                extra_classes = request.form["EC"]
                extra_classes_dict = {"No": 0, "Yes": 1}
                extra_activites = request.form["EA"]
                extra_activites_dict = {"No": 0, "Yes": 1}
                internet_access = request.form["IA"]
                internet_access_dict = {"No": 0, "Yes": 1}
                go_out = request.form["GO"]
                go_out_dict = {"Not Alot": 1, "Alot": 5}
                health = request.form["H"]
                health_dict = {"Bad": 1, "Good": 5}
                absent_days = request.form["AD"]
                array = np.array([[
                    int(gender),
                    int(age),
                    int(family_size_dict[family_size]),
                    int(mothers_education_dict[mothers_education]),
                    int(fathers_education_dict[fathers_education]),
                    int(mothers_job_dict[mothers_job]),
                    int(fathers_job_dict[fathers_job]),
                    int(guardian_dict[guardian]),
                    int(study_time),
                    int(exam_fails),
                    int(school_support_dict[school_support]),
                    int(family_support_dict[family_support]),
                    int(extra_classes_dict[extra_classes]),
                    int(extra_activites_dict[extra_activites]),
                    int(internet_access_dict[internet_access]),
                    int(go_out_dict[go_out]),
                    int(health_dict[health]),
                    int(absent_days),
                ]])
                array = array.reshape(1, -1)
                model = pickle.load(
                    open(
                        "./ML/student-mark-predictions-1/1st_term_test_predictions_model.pkl",
                        "rb",
                    ))
                result = model.predict(array)
                print(result)
                flash(
                    f"1st term Marks : {round(result[0][1])} | 2nd Term Marks : {round(result[0][2])} | 3rd Term Marks : {round(result[0][3])}",
                    "success",
                )
                return redirect("/Admin")
            else:
                return render_template("/admin/marks_predictions_t1.html",
                                       page="Marks")


@app.route(
    "/Admin/Predicting/Marks/T2",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Predicting/Marks/T2/",
    methods=["POST", "GET"],
)
def predicting_marks_t2():
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
                gender = request.form["Ge"]
                gender_dict = {"Female": 0, "Male": 1}
                gender = gender_dict[gender]
                age = int(request.form["A"])
                family_size = request.form["FS"]
                family_size_dict = {"Less Than 3": 1, "Bigger Than 3": 0}
                mothers_education = request.form["ME"]
                mothers_education_dict = {"None": 0, "Higher Education": 4}
                fathers_education = request.form["FE"]
                fathers_education_dict = {"None": 0, "Higher Education": 4}
                mothers_job = request.form["MJ"]
                mothers_job_dict = {
                    "At Home": 0,
                    "Health": 1,
                    "Other": 2,
                    "Services": 3,
                    "Teachers": 4,
                }
                fathers_job = request.form["FJ"]
                fathers_job_dict = {
                    "Teachers": 0,
                    "Other": 1,
                    "Services": 2,
                    "Health": 3,
                    "At Home": 4,
                }
                term_1_marks = request.form["T1"]
                guardian = request.form["G"]
                guardian_dict = {"Mother": 0, "Father": 1, "Other": 2}
                study_time = int(request.form["ST"])
                exam_fails = int(request.form["EF"])
                school_support = request.form["SS"]
                school_support_dict = {"Yes": 0, "No": 1}
                family_support = request.form["FSS"]
                family_support_dict = {"No": 0, "Yes": 1}
                extra_classes = request.form["EC"]
                extra_classes_dict = {"No": 0, "Yes": 1}
                extra_activites = request.form["EA"]
                extra_activites_dict = {"No": 0, "Yes": 1}
                internet_access = request.form["IA"]
                internet_access_dict = {"No": 0, "Yes": 1}
                go_out = request.form["GO"]
                go_out_dict = {"Not Alot": 1, "Alot": 5}
                health = request.form["H"]
                health_dict = {"Bad": 1, "Good": 5}
                absent_days = request.form["AD"]
                array = np.array([[
                    int(gender),
                    int(age),
                    int(family_size_dict[family_size]),
                    int(mothers_education_dict[mothers_education]),
                    int(fathers_education_dict[fathers_education]),
                    int(mothers_job_dict[mothers_job]),
                    int(fathers_job_dict[fathers_job]),
                    int(guardian_dict[guardian]),
                    int(study_time),
                    int(exam_fails),
                    int(school_support_dict[school_support]),
                    int(family_support_dict[family_support]),
                    int(extra_classes_dict[extra_classes]),
                    int(extra_activites_dict[extra_activites]),
                    int(internet_access_dict[internet_access]),
                    int(go_out_dict[go_out]),
                    int(health_dict[health]),
                    int(absent_days),
                    int(term_1_marks),
                ]])
                array = array.reshape(1, -1)
                model = pickle.load(
                    open(
                        "./ML/student-mark-predictions-1/2nd_term_test_predictions_model.pkl",
                        "rb",
                    ))
                result = model.predict(array)
                print("*" * 100)
                print(result)
                print("*" * 100)
                flash(
                    f"2nd Term Marks : {result[0][0]} | 3rd Term Marks : {result[0][1]}",
                    "success",
                )
                return redirect("/Admin")
            else:
                return render_template("/admin/marks_predictions_t2.html",
                                       page="Marks")


@app.route(
    "/Admin/Predicting/Marks/T3",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Predicting/Marks/T3/",
    methods=["POST", "GET"],
)
def predicting_marks_t3():
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
                gender = request.form["Ge"]
                gender_dict = {"Female": 0, "Male": 1}
                gender = gender_dict[gender]
                age = int(request.form["A"])
                family_size = request.form["FS"]
                family_size_dict = {"Less Than 3": 1, "Bigger Than 3": 0}
                mothers_education = request.form["ME"]
                mothers_education_dict = {"None": 0, "Higher Education": 4}
                fathers_education = request.form["FE"]
                fathers_education_dict = {"None": 0, "Higher Education": 4}
                mothers_job = request.form["MJ"]
                mothers_job_dict = {
                    "At Home": 0,
                    "Health": 1,
                    "Other": 2,
                    "Services": 3,
                    "Teachers": 4,
                }
                fathers_job = request.form["FJ"]
                fathers_job_dict = {
                    "Teachers": 0,
                    "Other": 1,
                    "Services": 2,
                    "Health": 3,
                    "At Home": 4,
                }
                term_1_marks = request.form["T1"]
                term_2_marks = request.form["T2"]
                guardian = request.form["G"]
                guardian_dict = {"Mother": 0, "Father": 1, "Other": 2}
                study_time = int(request.form["ST"])
                exam_fails = int(request.form["EF"])
                school_support = request.form["SS"]
                school_support_dict = {"Yes": 0, "No": 1}
                family_support = request.form["FSS"]
                family_support_dict = {"No": 0, "Yes": 1}
                extra_classes = request.form["EC"]
                extra_classes_dict = {"No": 0, "Yes": 1}
                extra_activites = request.form["EA"]
                extra_activites_dict = {"No": 0, "Yes": 1}
                internet_access = request.form["IA"]
                internet_access_dict = {"No": 0, "Yes": 1}
                go_out = request.form["GO"]
                go_out_dict = {"Not Alot": 1, "Alot": 5}
                health = request.form["H"]
                health_dict = {"Bad": 1, "Good": 5}
                absent_days = request.form["AD"]
                array = np.array([[
                    int(gender),
                    int(age),
                    int(family_size_dict[family_size]),
                    int(mothers_education_dict[mothers_education]),
                    int(fathers_education_dict[fathers_education]),
                    int(mothers_job_dict[mothers_job]),
                    int(fathers_job_dict[fathers_job]),
                    int(guardian_dict[guardian]),
                    int(study_time),
                    int(exam_fails),
                    int(school_support_dict[school_support]),
                    int(family_support_dict[family_support]),
                    int(extra_classes_dict[extra_classes]),
                    int(extra_activites_dict[extra_activites]),
                    int(internet_access_dict[internet_access]),
                    int(go_out_dict[go_out]),
                    int(health_dict[health]),
                    int(absent_days),
                    int(term_1_marks),
                    int(term_2_marks),
                ]])
                array = array.reshape(1, -1)
                model = pickle.load(
                    open(
                        "./ML/student-mark-predictions-1/3rd_term_test_predictions_model.pkl",
                        "rb",
                    ))
                result = model.predict(array)
                print("*" * 100)
                print(result)
                print("*" * 100)
                flash(
                    f"3rd Term Marks : {result[0][0]}",
                    "success",
                )
                return redirect("/Admin")
            else:
                return render_template("/admin/marks_predictions_t3.html",
                                       page="Marks")


@app.route(
    "/Admin/Predicting/Marks",
    methods=["POST", "GET"],
)
@app.route(
    "/Admin/Predicting/Marks/",
    methods=["POST", "GET"],
)
def predicting_marks():
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    if all(conditions):
        if session["Role"] == "Admin":
            return render_template("/admin/marks_predictions.html",
                                   page="Marks")
