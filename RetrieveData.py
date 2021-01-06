import json
import pathlib
import requests
import spacy
from datetime import date, timedelta

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
    t = date.today() - timedelta(days=1)
    tod = t.strftime("%Y-%m-%d")
    for country in countries:
        param.append({"date": tod, "name": country})
    return param


def getCOVIDResults(countries):
    url = getUrl(countries)
    world_url = "https://api.covid19api.com/world/total"
    result = {}

    try:
        response = requests.request("GET", url)
        resp = response.json()[len(response.json()) - 1]
        country = resp['Country']
        confirmed = resp['Confirmed']
        deaths = resp['Deaths']
        recovered = resp['Recovered']
        percent = round(float(deaths) / float(confirmed) * 100, 2)
        if "Korea" in country:
            country = "south korea"
        country_path = "/images/flaticon_countries/{}.png".format(country.lower().replace(" ", "-"))

        result['url'] = country_path
        result['name'] = country
        result['confirmed'] = confirmed
        result['deaths'] = deaths
        result['recovered'] = recovered
        result['percent'] = percent

    except Exception as e:
        result['worldFailed'] = True
        return None, False

    try:
        world_response = requests.request("GET", world_url)
        world_resp = world_response.json()
        total_deaths = world_resp['TotalDeaths']
        total_confirmed = world_resp['TotalConfirmed']
        result['totalConfirmed'] = total_confirmed
        result['totalDeaths'] = total_deaths
        result['totalRecovered'] = world_resp['TotalRecovered']
        death_percent = round(float(total_deaths) / float(total_confirmed) * 100, 2)
        result['totalPercent'] = death_percent

    except Exception as e:
        result['worldFailed'] = True
        return result, True

    result['worldFailed'] = False
    return result, True


if __name__ == '__main__':
    print(getCOVIDResults(["Italy"]))

