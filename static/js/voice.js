import {countries} from './countries.js'

// https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API

var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent

const grammar = '#JSGF V1.0; grammar countries; public <country> = ' + countries.join(' | ') + ' ;';

const recognition = new SpeechRecognition();
const speechRecognitionList = new SpeechGrammarList();
speechRecognitionList.addFromString(grammar, 1);
recognition.grammars = speechRecognitionList;
recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

var started = false;
var mic = document.getElementById("mic");
var info = document.getElementById("info");

mic.style.background = "linear-gradient(0.25turn, #ffe9c5, #fa9191)";

mic.onmouseover = function() {
    if (!started) {
        mic.style.background = "";
        mic.style.backgroundColor = "#ff577f";
    }
};

mic.onmouseleave = function() {
    if (!started) {
        mic.style.background = "linear-gradient(0.25turn, #ffe9c5, #fa9191)";
        mic.style.backgroundColor = "none";
    }
};

mic.onclick = function() {
	if (!started) {
	    recognition.start();
	    mic.classList.add("glow");
	    mic.style.background = "";
	    info.textContent = "Listening...";
	    started = true;
	} else {
	    recognition.stop();
	    mic.style.background = "linear-gradient(0.25turn, #ffe9c5, #fa9191)";
	    mic.classList.remove("glow");
	    info.textContent = "I'm ready!";
        started = false;
    }
};

async function getCountryName(result) {
    let response = await fetch(`${window.origin}/data`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(result),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })});
    let data = await response.json();
    var the_url = window.location.href;
    var new_url = the_url.split('/');
    new_url.pop();
    let name = data.name;
    if (name === "") {
        return new_url.join('/') + "/error";
    }
    return new_url.join('/') + "/country/" + name;
}

recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    info.textContent = 'Result received: ' + transcript + '.';
    let result = {"text": transcript};
    getCountryName(result).then((url) => {
            window.location.replace(url);
        })
        .catch(function (err) {
            var the_url = window.location.href;
            var new_url = the_url.split('/');
            new_url.pop();
            new_url = new_url.join('/') + "/error";
            window.location.replace(new_url);
        });
};

recognition.onspeechend = function() {
    recognition.stop();
    started = false;
};

recognition.onnomatch = function(event) {
    info.textContent = "I didn't recognise that country.";
};

recognition.onerror = function(event) {
    info.textContent = 'Error occurred in recognition: ' + event.error;
};
