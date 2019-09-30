$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-role").modal("show");
            },
            success: function (data) {
                $("#modal-role .modal-content").html(data.html_form);
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
                    $("#role-table tbody").html(data.html_role_list);
                    $("#modal-role").modal("hide");
                } else {
                    $("#modal-role .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create role
    $(".js-create-role").click(loadForm);
    $("#modal-role").on("submit", ".js-role-create-form", saveForm);

     // view role
     $("#role-table").on("click", ".js-view-role", loadForm);
    $("#modal-role").on("submit", ".js-role-view-form", saveForm);

    // Update role
    $("#role-table").on("click", ".js-update-role", loadForm);
    $("#modal-role").on("submit", ".js-role-update-form", saveForm);

    // Delete role
    $("#role-table").on("click", ".js-delete-role", loadForm);
    $("#modal-role").on("submit", ".js-role-delete-form", saveForm);

});