// Voice recognition functionality for LEO Voice Assistant
document.addEventListener('DOMContentLoaded', function() {
    const micButton = document.getElementById('micButton');
    const statusElement = document.getElementById('status');
    const userQueryElement = document.getElementById('userQuery');
    const assistantResponseElement = document.getElementById('assistantResponse');
    
    // Check if browser supports speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        
        let isListening = false;
        
        micButton.addEventListener('click', () => {
            if (!isListening) {
                // Start listening
                recognition.start();
                isListening = true;
                micButton.classList.add('listening');
                statusElement.textContent = 'Listening...';
            } else {
                // Stop listening
                recognition.stop();
                isListening = false;
                micButton.classList.remove('listening');
                statusElement.textContent = 'Ready to listen...';
            }
        });
        
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userQueryElement.textContent = transcript;
            statusElement.textContent = 'Processing...';
            
            // Send the transcript to the server for processing
            fetch('/process-query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: transcript }),
            })
            .then(response => response.json())
            .then(data => {
                assistantResponseElement.textContent = data.response;
                statusElement.textContent = 'Ready to listen...';
                
                // Text-to-speech for the response
                if ('speechSynthesis' in window) {
                    const utterance = new SpeechSynthesisUtterance(data.response);
                    utterance.rate = 1.0;
                    utterance.pitch = 1.0;
                    window.speechSynthesis.speak(utterance);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                assistantResponseElement.textContent = 'Sorry, I encountered an error processing your request.';
                statusElement.textContent = 'Ready to listen...';
            });
        };
        
        recognition.onend = () => {
            isListening = false;
            micButton.classList.remove('listening');
        };
        
        recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            statusElement.textContent = `Error: ${event.error}`;
            isListening = false;
            micButton.classList.remove('listening');
        };
    } else {
        statusElement.textContent = 'Speech recognition not supported in this browser.';
        micButton.disabled = true;
    }
});