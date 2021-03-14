$(document).ready(function(){
    $('form').on('click', '#button_dislike', function(){
        const serializedData = $("#like_form").serialize();
        const url = $("#button_dislike").data('url');
        const url_change = $("#button_dislike").data('url_change');

        $.ajax({
            type: 'POST',
            data: serializedData,
            url: url,
            success: function(response){
                $('#like_count').replaceWith(
                    '<div id="like_count"><p> Likes: ' + response['like'] + '</p></div>'
                );
                $('#button_dislike').replaceWith(
                     '<button type="button" class="btn btn-primary" id="button_like" ' +
                    'data-url_change="' + url + '" data-url="' + url_change + '">Like</button>'
                );
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            },
            });
        });
    });