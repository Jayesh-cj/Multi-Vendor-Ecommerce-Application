$(document).ready(function() {
    // Automatically close the alert after 5 seconds
    setTimeout(function() {
        $('popup-message').fadeOut(500, function() {
            $(this).remove();
        });
    }, 5000);

    // Close the alert when the close icon is clicked
    $('.alert-close-icon').click(function() {
        $(this).closest('.alert').fadeOut(200, function() {
            $(this).remove();
        });
    });
});