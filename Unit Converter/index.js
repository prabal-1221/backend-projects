function showForm(formNumber) {
    document.querySelectorAll('.buttons button').forEach(button => button.classList.remove('active'))
    document.querySelectorAll('.form-container').forEach(form => form.classList.remove('active'))

    document.getElementById(`btn${formNumber}`).classList.add('active')
    document.getElementById(`form${formNumber}`).classList.add('active')
}

function showResults(input, input_unit, output, output_unit) {
    const resultDiv = document.getElementById('results')
    const resultSpan = resultDiv.querySelector('span')
    resultSpan.textContent = String(input)+ ' ' + input_unit + ' = ' + String(output) + ' ' + output_unit
    resultDiv.classList.add('active')
}

function resetResults() {
    // document.getElementById('results').classList.remove('active')
    location.reload()
}

function handleFormLength(event) {
    event.preventDefault()
    const input = parseFloat(document.getElementById('input-length').value)
    const input_unit = document.getElementById('input-unit-length').value
    const output_unit = document.getElementById('input-unit-length').value
    const output = input ** 2
    showResults(input, input_unit, output, output_unit)
}

function handleFormWeight(event) {
    event.preventDefault()
    const input = parseFloat(document.getElementById('input-weight').value)
    const input_unit = document.getElementById('input-unit-weight').value
    const output_unit = document.getElementById('input-unit-weight').value
    const output = input ** 2
    showResults(input, input_unit, output, output_unit)
}

function handleFormTemperature(event) {
    event.preventDefault()
    const input = parseFloat(document.getElementById('input-temperature').value)
    const input_unit = document.getElementById('input-unit-temperature').value
    const output_unit = document.getElementById('input-unit-temperature').value
    const output = input ** 2
    showResults(input, input_unit, output, output_unit)
}