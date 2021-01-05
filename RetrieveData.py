import json
import pathlib
import requests
import spacy
from datetime import date, timedelta


# using https://rapidapi.com/Gramzivi/api/covid-19-data/discussions API to fetch COVID data
# using https://api.covid19api.com/total/country/ API to fetch COVID data
# https://documenter.getpostman.com/view/10808728/SzS8rjbc#27454960-ea1c-4b91-a0b6-0468bb4e6712
# only works on countries


nlp = spacy.load("en_core_web_sm")


def extractCountry(sentence):
    doc = nlp(sentence)
    for token in doc.ents:
        if token.label_ == 'GPE':
            return token.text

    return ""


def getConfig():
    file_name = "config"
    if not pathlib.Path(file_name).exists():
        return {
            'x-rapidapi-key': "",
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }
    with open(file_name) as f:
        config = json.load(f)
    return {
            'x-rapidapi-key': config["X-RapidAPI-Key"],
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }


def getUrl(country):
    url = "https://api.covid19api.com/total/country/"
    country = country.lower()
    country = country.replace(' ', '-')
    return url + country


def getParam(countries):
    param = []
    t = date.today() - timedelta(days=3)
    tod = t.strftime("%Y-%m-%d")
    for country in countries:
        param.append({"date": tod, "name": country})
    return param


def getCOVIDResults(countries):
    url = getUrl(countries)

    try:
        response = requests.request("GET", url)
        resp = response.json()[len(response.json()) - 1]
        result = {}
        country = resp['Country']
        confirmed = resp['Confirmed']
        deaths = resp['Deaths']
        recovered = resp['Recovered']
        percent = float(deaths) / float(confirmed) * 100

        result['name'] = country
        result['confirmed'] = confirmed
        result['deaths'] = deaths
        result['recovered'] = recovered
        result['percent'] = percent
    except Exception as e:
        return None, False

    return result, True


if __name__ == '__main__':
    print(getCOVIDResults(["Italy"]))

