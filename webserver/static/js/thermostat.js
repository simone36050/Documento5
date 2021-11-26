$(document).ready(function() {

    temperature = undefined
    umidity = undefined

    // get room id
    thermostat = parseInt($('#thermostat-id').html())

    // get data
    $.get('/api/device/' + encodeURIComponent(thermostat), function(data) {
        // set name
        $("#name").text(data.name)

        // set temperature
        temperature = data.temperature
        $("#temperature").val(data.temperature)

        // set umidity
        umidity = data.umidity
        $("#umidity").val(data.umidity)
    })

    // ok button handler
    $("#submit").click(function() {
        // change temperature
        new_temperature = parseInt($("#temperature").val())
        if(temperature != new_temperature) {
            $.post('/api/device/' + thermostat + '/thermostat/set_temperature/' + new_temperature)
        }

        // change umidity
        new_umidity = $("#umidity").val()
        if(umidity != new_umidity) {
            $.post('/api/device/' + thermostat + '/thermostat/set_umidity/' + new_umidity)
        }

        return false
    })

})