$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-smstemplate").modal("show");
            },
            success: function (data) {
                $("#modal-smstemplate .modal-content").html(data.html_form);
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
                    $("#smstemplate-table tbody").html(data.html_smstemplate_list);
                    $("#modal-smstemplate").modal("hide");
                } else {
                    $("#modal-smstemplate .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create smstemplate
    $(".js-create-smstemplate").click(loadForm);
    $("#modal-smstemplate").on("submit", ".js-smstemplate-create-form", saveForm);

     // view smstemplate
     $("#smstemplate-table").on("click", ".js-view-smstemplate", loadForm);
    $("#modal-smstemplate").on("submit", ".js-smstemplate-view-form", saveForm);

    // Update smstemplate
    $("#smstemplate-table").on("click", ".js-update-smstemplate", loadForm);
    $("#modal-smstemplate").on("submit", ".js-smstemplate-update-form", saveForm);

    // Delete smstemplate
    $("#smstemplate-table").on("click", ".js-delete-smstemplate", loadForm);
    $("#modal-smstemplate").on("submit", ".js-smstemplate-delete-form", saveForm);

});