$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-material").modal("show");
            },
            success: function (data) {
                $("#modal-material .modal-content").html(data.html_form);
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
                    $("#material-table tbody").html(data.html_material_list);
                    $("#modal-material").modal("hide");
                } else {
                    $("#modal-material .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create material
    $(".js-create-material").click(loadForm);
    $("#modal-material").on("submit", ".js-material-create-form", saveForm);

     // view material
     $("#material-table").on("click", ".js-view-material", loadForm);
    $("#modal-material").on("submit", ".js-material-view-form", saveForm);

    // Update material
    $("#material-table").on("click", ".js-update-material", loadForm);
    $("#modal-material").on("submit", ".js-material-update-form", saveForm);

    // Delete material
    $("#material-table").on("click", ".js-delete-material", loadForm);
    $("#modal-material").on("submit", ".js-material-delete-form", saveForm);

});