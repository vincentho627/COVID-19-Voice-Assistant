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

// const diagnostic = document.querySelector('.output');
var started = false;
var mic = document.getElementById("mic");

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
	    console.log('Ready to receive a country.');
	    mic.classList.add("glow");
	    mic.style.background = "";
	    started = true;
	} else {
	    recognition.stop();
	    mic.style.background = "linear-gradient(0.25turn, #ffe9c5, #fa9191)";
	    mic.classList.remove("glow");
	    console.log('Paused.');
        started = false;
    }
};

recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    // diagnostic.textContent = 'Result received: ' + transcript + '.';
    let result = {"text": transcript};
    fetch(`${window.origin}/data`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(result),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        }),
        redirect: 'follow',
    }).then(response => {
        console.log(response);
        window.location.replace(response.url);
    }).catch(function(err) {
        console.info(err + " url: " + url);
    });
    console.log('Confidence: ' + event.results[0][0].confidence);
};

recognition.onspeechend = function() {
    recognition.stop();
    document.getElementById("select").classList.remove("glow");
    started = false;
};

// recognition.onnomatch = function(event) {
//     diagnostic.textContent = "I didn't recognise that country.";
// };

// recognition.onerror = function(event) {
//     diagnostic.textContent = 'Error occurred in recognition: ' + event.error;
// };