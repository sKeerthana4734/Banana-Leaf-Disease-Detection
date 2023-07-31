const detectButton = document.getElementById('detect-button');
const goBackButton = document.getElementById('goBack-button');
const detectSection = document.getElementById('detect');
const imageInput = document.getElementById('image');
const predictButton = document.getElementById('predict-button');
const loadingDiv = document.getElementById('loading');
const resultDiv = document.getElementById('result');
const resultImage = document.getElementById('result-image');
const resultText = document.getElementById('result-text');
const causes = document.getElementById('causes');
const prevention = document.getElementById('prevention');

detectButton.addEventListener('click', () => {
    detectSection.classList.remove('hidden');
});

goBackButton.addEventListener('click', () => {
    window.location.href = "http://127.0.0.1:5000/";
});

predictButton.addEventListener('click', (event) => {
    event.preventDefault();
    loadingDiv.classList.remove('hidden');
    resultDiv.classList.add('hidden');
    const formData = new FormData();
    formData.append('image', imageInput.files[0]);
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            loadingDiv.classList.add('hidden');
            resultDiv.classList.remove('hidden');
            // resultImage.src = URL.createObjectURL(imageInput.files[0]);
            console.log(data);
            resultText.textContent = data['disease'];
            causes.textContent = data['causes'];
            prevention.textContent = data['prevention'];
        })
        .catch(error => {
            loadingDiv.classList.add('hidden');
            alert('Error occurred: ' + error);
        });
});
