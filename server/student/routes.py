from server import *
from server.db.admin.crud_subjects import *
from server.db.admin.crud_users import *
from server.db.notices import *
from server.db.admin.files import *
from server.db.admin.stream import *

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


@app.route("/Student/Notices")
@app.route("/Student/Notices/")
@app.route("/Student/Notice")
@app.route("/Student/Notice/")
def student_notices():
    try:
        conditions = [
            "Auth" in session,
            "User Name" in session,
            "Password or Email" in session,
            "Role" in session,
            "Returned Data" in session,
            session["Role"] == "Student",
        ]
        if all(conditions):
            info = get_notices()
            return render_template("/student/student_notices.html", notices=info)
        return abort(404)
    except:
        return abort(505)


@app.route("/Student/File")
@app.route("/Student/Files/")
@app.route("/Student/Files")
@app.route("/Student/File/")
def student_file():
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
        session["Role"] == "Student",
    ]
    if all(conditions):
        f = File_Admin(file="", description="")
        file_types = f.get_all_file_types()
        return render_template("/student/files.html", file_types=file_types)
    return abort(404)


@app.route("/Student/File/<string:file_type>")
@app.route("/Student/Files/<string:file_type>")
@app.route("/Student/Files/<string:file_type>/")
@app.route("/Student/File/<string:file_type>/")
def student_files(file_type):
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
        session["Role"] == "Student",
    ]
    if all(conditions):
        f = File_Admin(file="", description="")
        files = f.get_all_files_in_a_file_type(file_type)
        return render_template(
            "/student/file.html", files=files, file_type=file_type
        )
    return abort(404)

@app.route(
    "/Student/File/<string:file_type>/<string:filename>/<string:desc>/Download/",
    methods=["POST", "GET"],
)
@app.route(
    "/Student/File/<string:file_type>/<string:filename>/<string:desc>/Download",
    methods=["POST", "GET"],
)
def file_type_download_student(file_type, filename, desc):
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
    if all(conditions) and session["Role"] == "Student":
        f = File_Admin(file="", description=desc)
        result = f.get(
            file_type_name=file_type,
            description=desc,
            filename=filename,
        )
        print("*+" * 100)
        print(result)
        print("*+" * 100)
        return send_from_directory(
            result[0], filename=result[1], as_attachment=True
        )


@app.route(
    "/Student/File/<string:file_type>/<string:filename>/<string:desc>/View/",
    methods=["POST", "GET"],
)
@app.route(
    "/Student/File/<string:file_type>/<string:filename>/<string:desc>/View",
    methods=["POST", "GET"],
)
def file_type_view_student(file_type, filename, desc):
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
    if all(conditions) and session["Role"] == "Student":
        f = File_Admin(file="", description=desc)
        result = f.get(
            file_type_name=file_type,
            description=desc,
            filename=filename,
        )
        return send_from_directory(
            result[0], filename=result[1], as_attachment=False
        )

@app.route(
    "/Student/Chat",
    methods=["POST", "GET"],
)
@app.route(
    "/Student/Chat/",
    methods=["POST", "GET"],
)
def chat():
    conditions = [
        "Auth" in session,
        "User Name" in session,
        "Password or Email" in session,
        "Role" in session,
        "Returned Data" in session,
    ]
    print("OK")
    if all(conditions) and session["Role"] == "Student":
        if request.method == 'POST':
            message = request.form["M"]
            s = Stream(
                message=message,
                user_name=session["User Name"],
                role=session["Role"],
            )
            s.add()
            return redirect("/Student/Chat")
        else:
            messages = Stream(message="", user_name="", role="")
            messages = messages.get()
            messages = messages[::-1]
            return render_template(
                "/student/chat.html",
                page="Chat",
                messages=messages,
                user_name=session["User Name"],
            )

