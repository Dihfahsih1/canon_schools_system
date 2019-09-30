$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-emailsetting").modal("show");
            },
            success: function (data) {
                $("#modal-emailsetting .modal-content").html(data.html_form);
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
                    $("#emailsetting-table tbody").html(data.html_emailsetting_list);
                    $("#modal-emailsetting").modal("hide");
                } else {
                    $("#modal-emailsetting .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create emailsetting
    $(".js-create-emailsetting").click(loadForm);
    $("#modal-emailsetting").on("submit", ".js-emailsetting-create-form", saveForm);

     // view emailsetting
     $("#emailsetting-table").on("click", ".js-view-emailsetting", loadForm);
    $("#modal-emailsetting").on("submit", ".js-emailsetting-view-form", saveForm);

    // Update emailsetting
    $("#emailsetting-table").on("click", ".js-update-emailsetting", loadForm);
    $("#modal-emailsetting").on("submit", ".js-emailsetting-update-form", saveForm);

    // Delete emailsetting
    $("#emailsetting-table").on("click", ".js-delete-emailsetting", loadForm);
    $("#modal-emailsetting").on("submit", ".js-emailsetting-delete-form", saveForm);

});