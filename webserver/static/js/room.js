$(document).ready(function() {

    // get room id
    room = parseInt($('#room-id').html())

    // get data
    $.get('/api/room/' + encodeURIComponent(room), function(data) {
        // set name
        $("#name").text(data.name)

        // set devices
        devices = data.devices
        for(let i = 0; i < devices.length; i++) {
            // create tag
            $(
                `   <li>
                        <a href="{url}">{name}</a>
                    </li>
                `.replace('{url}', '/device/' + devices[i].id)
                 .replace('{name}', devices[i].name)
            ).appendTo('#devices')
        }
    })

})