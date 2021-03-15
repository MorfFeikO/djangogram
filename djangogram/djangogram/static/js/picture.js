$(document).ready(function() {
    $('form').on('click', '#button_picture', function () {
        const serializedData = $("#picture_form").serialize();
        const url = $("#picture_form").data('url')
        const csrftoken = $('#picture_form').serializeArray()[0]['value']
        console.log(serializedData);
        console.log(url);
        console.log(csrftoken)

        $.ajax({
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data: serializedData,
            url: url,
            processData: false,
            contentType: false,
            success: function(response){
                console.log(response)
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            },
            });
        });
    });