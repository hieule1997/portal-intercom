$(document).ready(function () {
    // get data nations and states
    $.ajax({
        type: "GET",
        url: "/json-nations-states",
        success: data => {
            countries = data.countries
            var element = ``
            countries.map(item => {
                element += `<option value=${item.country}>${item.country}</option>`
            })
            $('.crs-country').html(element)
            $('.crs-country').change( () => {
                var currentCountry = $('.crs-country').val()
                var state = countries.find(element => element.country === currentCountry)
                state = state.states
                var element = ``
                state.map( item => {
                    element += `<option value=${item}>${item}</option>`
                } )
                $('#region').html(element)
            })
        }
    })

    // get data time zone
    $.ajax({
        type: "GET",
        url: "/timezone",
        success: data => {
            var element = ``
            data.map( item => {
                element += `<option value=${item.value}>${item.text}</option>`
            } )
            $('#timezone').html(element)
        }
    })
})