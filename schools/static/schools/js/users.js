$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-user").modal("show");
            },
            success: function (data) {
                $("#modal-user .modal-content").html(data.html_form);
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
                    $("#user-table tbody").html(data.html_user_list);
                    $("#modal-user").modal("hide");
                } else {
                    $("#modal-user .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create user
    $(".js-create-user").click(loadForm);
    $("#modal-user").on("submit", ".js-user-create-form", saveForm);

     // view user
     $("#user-table").on("click", ".js-view-user", loadForm);
    $("#modal-user").on("submit", ".js-user-view-form", saveForm);

    // Update user
    $("#user-table").on("click", ".js-update-user", loadForm);
    $("#modal-user").on("submit", ".js-user-update-form", saveForm);

    // Delete user
    $("#user-table").on("click", ".js-delete-user", loadForm);
    $("#modal-user").on("submit", ".js-user-delete-form", saveForm);

});