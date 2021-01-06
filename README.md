# COVID-19-Voice-Assistant

Introduction
------------
COVID-19 is a disease caused by a new strain of coronavirus and has effected all of us throughout 2020. Everyday, cases keep rising around the world and it has become hard to keep track on which countries are doing well against this pandemic. So I created a webapp that allows you, the user to check cases in countries around the world and see how they are handling COVID-19. This webapp uses Python for the backend and Javascript, HTML and CSS for the frontend.

![](static/images/intro.png)

Installing Packages
-------------------
Packages used:

```python
import spacy
from flask import Flask, render_template, redirect, request
```

Installing package, run:

```terminal
pip install flask, spacy
```

Run Server
----------
To run the server: 

```
flask run
```

How to use the webapp
=====================

Voice Assistant
---------------
This webapp is not any ordinary, it allows you to speak to the webapp to get the information you want using voice recognition. A simple example could be saying "can I have the cases for China", the webapp will then convert the speech to plain text using Javascript which is then fed to a nlp to extract key informations using Python, in this case, a country.

![](static/images/voiceAssistant.png)

Manual Inputs
-------------
If voice recognition is not your thing, you can always use the manual option to input the country you want. The result will be the same!

![](static/images/manualInputs.png)

Results
-------
After choosing your countries with either option. Results of that country will be displayed on the screen along with the world-wide total results.

![](static/images/result.png)

Resources
---------
APIs used to retrieve statistics: https://documenter.getpostman.com/view/10808728/SzS8rjbc#27454960-ea1c-4b91-a0b6-0468bb4e6712

Country icons: https://www.flaticon.com/packs/countrys-flags

