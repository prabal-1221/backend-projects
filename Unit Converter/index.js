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

function convertToMeter(input, input_unit) {
    switch(input_unit) {
        case 'Metre':
            return input
        case 'Kilometer':
            return input*1000
        case 'Centimeter':
            return input*0.01
        case 'Millimeter':
            return input*0.001
        case 'Micrometer':
            return input*1e-6
        case 'Nanometer':
            return input*1e-9
        case 'Mile':
            return input*1609.34
        case 'Yard':
            return input*0.9144
        case 'Foot':
            return input*0.3048
        case 'Inch':
            return input*0.0254
        case 'Nautical mile':
            return input*1852
    }
}

function convertFromMeter(input, output_unit) {
    switch(output_unit) {
        case 'Metre':
            return input
        case 'Kilometer':
            return input*0.001
        case 'Centimeter':
            return input*100
        case 'Millimeter':
            return input*1000
        case 'Micrometer':
            return input*1e+6
        case 'Nanometer':
            return input*1e+9
        case 'Mile':
            return input*0.000621371
        case 'Yard':
            return input*1.09361
        case 'Foot':
            return input*3.28084
        case 'Inch':
            return input*39.3701
        case 'Nautical mile':
            return input*0.000539957
    }
}

function handleFormLength(event) {
    event.preventDefault()
    const input = parseFloat(document.getElementById('input-length').value)
    const input_unit = document.getElementById('input-unit-length').value
    const output_unit = document.getElementById('output-unit-length').value
    var input_in_meter = convertToMeter(input, input_unit)
    var final_output = convertFromMeter(input_in_meter, output_unit)
    showResults(input, input_unit, final_output, output_unit)
}

function convertToGram(input, input_unit) {
    switch(input_unit) {
        case 'Tonne':
            return input*1e+6
        case 'Kilogram':
            return input*1000
        case 'Gram':
            return input
        case 'Milligram':
            return input*0.001
        case 'Microgram':
            return input*1e-6
        case 'Imperial ton':
            return input*1.016e+6
        case 'US ton':
            return input*907185
        case 'Stone':
            return input*6350.29
        case 'Pound':
            return input*453.592
        case 'Ounce':
            return input*28.3495
    }
}

function convertFromGram(input, output_unit) {
    switch(output_unit) {
        case 'Tonne':
            return input*1e-6
        case 'Kilogram':
            return input*0.001
        case 'Gram':
            return input
        case 'Milligram':
            return input*1000
        case 'Microgram':
            return input*1e+6
        case 'Imperial ton':
            return input*9.8421e-7
        case 'US ton':
            return input*1.1023e-6
        case 'Stone':
            return input*0.000157473
        case 'Pound':
            return input*0.00220462
        case 'Ounce':
            return input*0.035274
    }
}

function handleFormWeight(event) {
    event.preventDefault()
    const input = parseFloat(document.getElementById('input-weight').value)
    const input_unit = document.getElementById('input-unit-weight').value
    const output_unit = document.getElementById('output-unit-weight').value
    var input_in_gram = convertToGram(input, input_unit)
    var final_output = convertFromGram(input_in_gram, output_unit)
    showResults(input, input_unit, final_output, output_unit)
}

function convertToDegreeCelsius(input, input_unit) {
    switch(input_unit) {
        case 'Degree Celsius':
            return input
        case 'Fahrenheit':
            return ((input - 32)*5)/9
        case 'Kelvin':
            return input - 273.15
    }
}
        
function convertFromDegreeCelsius(input, output_unit) {
    switch(output_unit) {
        case 'Degree Celsius':
            return input
        case 'Fahrenheit':
            return input*1.8 + 32
        case 'Kelvin':
            return input + 273.15
    }
}

function handleFormTemperature(event) {
    event.preventDefault()
    const input = parseFloat(document.getElementById('input-temperature').value)
    const input_unit = document.getElementById('input-unit-temperature').value
    const output_unit = document.getElementById('output-unit-temperature').value
    var input_in_celsius = convertToDegreeCelsius(input, input_unit)
    console.log(input_in_celsius)
    var final_output = convertFromDegreeCelsius(input_in_celsius, output_unit)
    showResults(input, input_unit, final_output, output_unit)
}