$(document).ready(function(){
    $('form').on('click', '#button_befriend', function(){
        const serializedData = $("#friend_form").serialize();
        const url = $("#button_befriend").data('url');
        const url_change = $("#button_befriend").data('url_change');

        $.ajax({
            type: 'POST',
            data: serializedData,
            url: url,
            success: function(response){
                $('#button_befriend').replaceWith(
                     '<button type="button" class="btn btn-light" id="button_nofriend" ' +
                    'data-url_change="' + url + '" data-url="' + url_change + '">Remove friend</button>'
                );
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            },
            });
        });
    });