from flask import Flask, render_template, redirect, request

from ExtractKeyInfo import extractCountry
from RetrieveData import getCOVIDResults

app = Flask(__name__, template_folder='templates')
result = None
voice = False


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/data", methods=["GET", "POST"])
def getData():
    global result, voice
    if request.method == "POST":
        req = request.get_json()
        if req and 'text' in req:
            voice = True
            country = extractCountry(req['text'])
        else:
            country = request.form['country']

        print(country)
        result, success = getCOVIDResults(country)
        if success:
            return render_template("country.html", country=result)
        else:
            return render_template("error.html", country=result)
    else:
        if voice:
            if result:
                voice = False
                return render_template("country.html", country=result)
            else:
                return render_template("error.html", country=result)
        else:
            return redirect("/")


if __name__ == '__main__':
    app.run()

