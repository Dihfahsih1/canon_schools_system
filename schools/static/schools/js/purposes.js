$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-purpose").modal("show");
            },
            success: function (data) {
                $("#modal-purpose .modal-content").html(data.html_form);
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
                    $("#purpose-table tbody").html(data.html_purpose_list);
                    $("#modal-purpose").modal("hide");
                } else {
                    $("#modal-purpose .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create purpose
    $(".js-create-purpose").click(loadForm);
    $("#modal-purpose").on("submit", ".js-purpose-create-form", saveForm);

     // view purpose
     $("#purpose-table").on("click", ".js-view-purpose", loadForm);
    $("#modal-purpose").on("submit", ".js-purpose-view-form", saveForm);

    // Update purpose
    $("#purpose-table").on("click", ".js-update-purpose", loadForm);
    $("#modal-purpose").on("submit", ".js-purpose-update-form", saveForm);

    // Delete purpose
    $("#purpose-table").on("click", ".js-delete-purpose", loadForm);
    $("#modal-purpose").on("submit", ".js-purpose-delete-form", saveForm);

});