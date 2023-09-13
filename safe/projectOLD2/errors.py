from flask import redirect, render_template, url_for, flash


from project import app


@app.errorhandler(404)
def error_404(error):

    return redirect("/")


@app.errorhandler(500)
def error_500(error):

    error = "500"
    message = "Something Went Wrong"

    return render_template("error.html", error=error, message=message), 500


def _Error(message, error=0):
    if error != 0:
        error = error=f"Error: {error}"
    else:
        error = "Error:"

    return render_template("error.html", error=error, message=message)


def _Flash(message, route="/"):

    flash(message)
    return redirect(route)
