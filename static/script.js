async function predictDisease() {

    const data = {
        age: document.getElementById('age').value,
        sex: document.getElementById('sex').value,
        chestPain: document.getElementById('chestPain').value,
        restingBP: document.getElementById('restingBP').value,
        cholesterol: document.getElementById('cholesterol').value,
        fastingBS: document.getElementById('fastingBS').value,
        restingECG: document.getElementById('restingECG').value,
        maxHR: document.getElementById('maxHR').value,
        exerciseAngina: document.getElementById('exerciseAngina').value,
        oldpeak: document.getElementById('oldpeak').value,
        stSlope: document.getElementById('stSlope').value
    }

    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }, body: JSON.stringify(data)
    })

    const result = await response.json()

    const resultDiv = document.getElementById('result')

    resultDiv.innerHTML = `
        ${result.prediction}<br><br>
        Confidence: ${result.probability}%
    `

    if(result.prediction.includes('High')) {
        resultDiv.style.background = '#7f1d1d' }
    else {
        resultDiv.style.background = '#14532d'
    }
}