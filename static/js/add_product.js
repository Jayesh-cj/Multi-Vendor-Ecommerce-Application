$(document).ready(function () {
    let formCount = $('#id_form-TOTAL_FORMS').val();

    // Function to add a new image form
    function addImageForm() {
        const newForm = $('.image-form').first().clone();
        const formRegex = /form-(\d){1}-/g;

        // Update the new form's input names and IDs
        newForm.html(newForm.html().replace(formRegex, `form-${formCount}-`));

        // Clear the input value and append the form to the container
        newForm.find('input[type="file"]').val('');
        newForm.find('input[type="checkbox"]').prop('checked', false);
        $('#image-formset').append(newForm);

        // Update the total forms count
        formCount++;
        $('#id_form-TOTAL_FORMS').val(formCount);
    }

    // Event listener for adding a new image form
    $('#add-image').click(function () {
        addImageForm();
    });

    // Event listener for removing an image form
    $('#image-formset').on('click', '.remove-image', function () {
        $(this).closest('.image-form').remove();
        formCount--;
        $('#id_form-TOTAL_FORMS').val(formCount);
    });
});