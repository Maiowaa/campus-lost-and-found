$(document).ready(function () {

    // Image preview on file upload
    $('#id_image').on('change', function () {
        var file = this.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#image-preview').html(
                    '<img src="' + e.target.result + '" class="img-thumbnail mt-2" style="max-height:200px;">'
                );
            };
            reader.readAsDataURL(file);
        }
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function () {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Live search filter on item list (client-side filtering)
    $('#id_query').on('keyup', function () {
        var query = $(this).val().toLowerCase();
        if (query.length >= 2) {
            $('.item-card').each(function () {
                var text = $(this).text().toLowerCase();
                $(this).closest('.col-md-4').toggle(text.indexOf(query) > -1);
            });
        } else {
            $('.item-card').closest('.col-md-4').show();
        }
    });

});
