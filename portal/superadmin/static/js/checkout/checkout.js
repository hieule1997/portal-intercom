$(document).ready(function () {

    var country_state = ""

    // get data nations and states
    $.ajax({
        type: "GET",
        url: "/json-nations-states",
        success: data => {
            country_state = data
            var countries = data
            var element = ``
            countries.map(item => {
                element += `<option value=${item.country_code}>${item.country_name}</option>`
            })
            $('.crs-country').html(element)
            $('.crs-country').change(() => {
                var currentCountry = $('.crs-country').val()
                var region = countries.find(element => element.country_code === currentCountry)
                region = region.country_region
                var element = ``
                region.map(item => {
                    element += `<option value=${item.region_code}>${item.region_name}</option>`
                })
                $('#region').html(element)
            })

            // get data time zone
            $.ajax({
                type: "GET",
                url: "/timezone",
                success: data => {
                    var element = ``
                    data.map(item => {
                        element += `<option value=${item.value}>${item.text}</option>`
                    })
                    $('#timezone').html(element)
                }
            })


            $.ajax({
                type: "GET",
                url: "/data-user-json",
                success: data => {
                    var region = country_state.find(item => item.country_code === data.country)
                    $(`[name=country] option[value=${data.country}]`).prop('selected', true);
                    region = region.country_region
                    var element = ``
                    region.map(item => {
                        element += `<option value=${item.region_code}>${item.region_name}</option>`
                    })
                    $('#region').html(element)
                    $('#region').val(data.region)
                    $('#timezone').val(data.timezone)

                    $('#lastname').val(data.fullname)
                    $('#email').val(data.email)
                    $('#phone').val(data.phone)
                    $('#companyname').val(data.company)
                    $('#director').val(data.company)
                    $('#tax-id').val(data.tax_id)
                    $('#address1').val(data.address1)
                    $('#city').val(data.city)
                    $('#address2').val(data.address2)
                    $('#postcode').val(data.post_code)
                }
            })
        }
    })

    // Click update
    $('#btUpdate').on('click', (e) => {
        e.preventDefault()
        var region = $('#region').val()
        var timezone = $('#timezone').val()

        var latname = $('#lastname').val()
        var email = $('#email').val()
        var phone = $('#phone').val()
        var company_name = $('#companyname').val()
        var director = $('#director').val()
        var tax_id = $('#tax-id').val()
        var address1 = $('#address1').val()
        var city = $('#city').val()
        var address2 = $('#address2').val()
        var postcode = $('#postcode').val()
    })
})