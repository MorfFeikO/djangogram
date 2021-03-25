$(document).ready(function(){
    $('form').on('click', '#button_nofriend', function(){
        const serializedData = $("#friend_form").serialize();
        const url = $("#button_nofriend").data('url');
        const url_change = $("#button_nofriend").data('url_change');

        $.ajax({
            type: 'POST',
            data: serializedData,
            url: url,
            success: function(response){
                $('#button_nofriend').replaceWith(
                     '<button type="button" class="btn btn-success" id="button_befriend" ' +
                    'data-url_change="' + url + '" data-url="' + url_change + '">Add friend</button>'
                );
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            },
            });
        });
    });