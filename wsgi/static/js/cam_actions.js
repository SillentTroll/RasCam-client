$(document).ready(function () {

    $('#reset_confirm_modal').on('show.bs.modal', function () {
        $('.alert').hide();
    })

});

function reset_camera(){
    $('.alert').hide();
    $.getJSON(cam_actions_url.reset_cam, {'confirmation': 'yes',
                                          'camera_name': $('#reset_camera_name').val()},
                function (data) {
                    if (data.result == "OK") {
                        location.reload();
                    } else {
                        $('#reset_alerts').html(data.error);
                        $('.alert').show();
                    }
                });
}