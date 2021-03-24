$(document).ready(function() {
    $('form').on('click', '#button_picture', function () {
        const serializedData = $("#picture_form").serialize();
        const url = $("#picture_form").data('url');
        const csrftoken = $('#picture_form').serializeArray()[0]['value'];
        var csrftok = $('#picture_form').get(0)[0]['value'];
        var picture = $('#picture_form').get(0)[1].files[0];
        var title = $('#picture_form').get(0)[2]['value'];
        var dat = new FormData()
        dat.append('picture', picture);
        dat.append('picture_title', title)

        $.ajax({
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data: dat,
            url: url,
            enctype: 'multipart/form-data',
            processData: false,
            contentType: false,

            success: function(response){
                if($('#picture_column').length){
                    $('#picture_column').prepend(
                        '<div class="row shadow-sm p-3 mb-5 bg-white rounded" id="picture_column">' +
                        '<div class="col-md"><p><img src="' + response['picture']['url'] +
                        '" alt="OOOps, where is picture?" width="150" height="180"></p></div>' +
                        '<div class="col-md"><p>Title: ' + response['picture']['picture_title'] +
                        '</p><p>Public date: ' + response['picture']['pub_date'] + '</p>' +
                        '<div id="like_count"><p> Likes: ' + response['picture']['total_likes'] + '</p></div></div></div>'
                    );
                }
                else {
                    $('#img_div').append(
                        '<div class="row shadow-sm p-3 mb-5 bg-white rounded" id="picture_column">' +
                        '<div class="col-md"><p><img src="' + response['picture']['url'] +
                        '" alt="OOOps, where is picture?" width="150" height="180"></p></div>' +
                        '<div class="col-md"><p>Title: ' + response['picture']['picture_title'] +
                        '</p><p>Public date: ' + response['picture']['pub_date'] + '</p>' +
                        '<div id="like_count"><p> Likes: ' + response['picture']['total_likes'] + '</p></div></div></div>'
                    );
                }
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            },
            });
        $('#picture_form')[0].reset();
        });
    });