from flask import Flask, render_template, redirect, request

from RetrieveData import getCOVIDResults

app = Flask(__name__, template_folder='templates')


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/data", methods=["GET", "POST"])
def getData():
    if request.method == "POST":
        country = request.form['country']
        countries, success = getCOVIDResults([country])
        if success:
            return render_template("country.html", countries=countries)
        else:
            return render_template("error.html", countries=countries)
    else:
        return redirect("/")


if __name__ == '__main__':
    app.run()

