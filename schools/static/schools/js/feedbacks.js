$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-feedback").modal("show");
            },
            success: function (data) {
                $("#modal-feedback .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        var formData = new FormData(form[0]);
        $.ajax({
            url: form.attr("action"),
            data: formData,
            type: form.attr("method"),
            dataType: 'json',
            async: true,
            cache: false,
            contentType: false,
            enctype: form.attr("enctype"),
            processData: false,
            success: function (data) {
                if (data.form_is_valid) {
                    $("#feedback-table tbody").html(data.html_feedback_list);
                    $("#modal-feedback").modal("hide");
                } else {
                    $("#modal-feedback .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create feedback
    $(".js-create-feedback").click(loadForm);
    $("#modal-feedback").on("submit", ".js-feedback-create-form", saveForm);

     // view feedback
     $("#feedback-table").on("click", ".js-view-feedback", loadForm);
    $("#modal-feedback").on("submit", ".js-feedback-view-form", saveForm);

    // Update feedback
    $("#feedback-table").on("click", ".js-update-feedback", loadForm);
    $("#modal-feedback").on("submit", ".js-feedback-update-form", saveForm);

    // Delete feedback
    $("#feedback-table").on("click", ".js-delete-feedback", loadForm);
    $("#modal-feedback").on("submit", ".js-feedback-delete-form", saveForm);

});