import json

from flask import Flask, render_template, redirect, request, url_for

from RetrieveData import getCOVIDResults, extractCountry

app = Flask(__name__, template_folder='templates')


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/voice")
def voice():
    return render_template("voice.html")


@app.route("/manual")
def manual():
    return render_template("manual.html")


@app.route("/error")
def error():
    return render_template("error.html")


@app.route("/<country>")
def result(country):
    res, success = getCOVIDResults(country)
    if success:
        return render_template("country.html", country=res)
    else:
        return render_template("error.html", country=result)


@app.route("/data", methods=["POST"])
def getData():
    req = request.get_json()
    if req and 'text' in req:
        country = extractCountry(req['text'])
        res = {"name": country}
        response = app.response_class(
            response=json.dumps(res),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        country = request.form['country']
        return redirect(url_for("result", country=country))


if __name__ == '__main__':
    app.run()

