$(document).ready(function(){
    $('form').on('click', '#button_like', function(){
        const serializedData = $("#like_form").serialize();
        const url = $("#button_like").data('url');
        const url_change = $("#button_like").data('url_change');

        $.ajax({
            type: 'POST',
            data: serializedData,
            url: url,
            success: function(response){
                $('#like_count').replaceWith(
                    '<div id="like_count"><p> Likes: ' + response['like'] + '</p></div>'
                );
                $('#button_like').replaceWith(
                     '<button type="button" class="btn btn-danger" id="button_dislike" ' +
                    'data-url_change="' + url + '" data-url="' + url_change + '">Dislike</button>'
                );
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            },
            });
        });
    });