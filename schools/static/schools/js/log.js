$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-log").modal("show");
            },
            success: function (data) {
                $("#modal-log .modal-content").html(data.html_form);
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
                    $("#log-table tbody").html(data.html_log_list);
                    $("#modal-log").modal("hide");
                } else {
                    $("#modal-log .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create log
    $(".js-create-log").click(loadForm);
    $("#modal-log").on("submit", ".js-log-create-form", saveForm);

    // view log
    $("#log-table").on("click", ".js-view-log", loadForm);
    $("#modal-log").on("submit", ".js-log-view-form", saveForm);

    // Update log
    $("#log-table").on("click", ".js-update-log", loadForm);
    $("#modal-log").on("submit", ".js-log-update-form", saveForm);

    // Delete log
    $("#log-table").on("click", ".js-delete-log", loadForm);
    $("#modal-log").on("submit", ".js-log-delete-form", saveForm);

});