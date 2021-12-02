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
                `   <li class="list-group-item list-group-item-action row mt-3 border rounded">
                        <a class="text-decoration-none md-v-line h5" href="{url}"> <span>{name}</span> </a>
                    </li>
                `.replace('{url}', '/device/' + devices[i].id)
                 .replace('{name}', devices[i].name)
            ).appendTo('#devices')
        }
    })

})