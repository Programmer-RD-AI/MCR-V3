from server import *


@app.errorhandler(404)
def page_not_found(self):
    return render_template("/error/404.html")


@app.errorhandler(505)
def server_error(self):
    return render_template("/error/505.html")
