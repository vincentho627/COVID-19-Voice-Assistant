import countries from './countries.js'

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

const diagnostic = document.querySelector('.output');
var started = false;

document.body.onclick = function() {
	if (!started) {
	  recognition.start();
	  console.log('Ready to receive a country.');
	  started = true;
	}
};

recognition.onresult = function(event) {
  const country = event.results[0][0].transcript;
  diagnostic.textContent = 'Result received: ' + country + '.';
  console.log('Confidence: ' + event.results[0][0].confidence);
};

recognition.onspeechend = function() {
  recognition.stop();
  started = false;
};

recognition.onnomatch = function(event) {
  diagnostic.textContent = "I didn't recognise that country.";
};

recognition.onerror = function(event) {
  diagnostic.textContent = 'Error occurred in recognition: ' + event.error;
};