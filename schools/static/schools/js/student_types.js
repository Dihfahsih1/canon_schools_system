$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-student_type").modal("show");
            },
            success: function (data) {
                $("#modal-student_type .modal-content").html(data.html_form);
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
                    $("#student_type-table tbody").html(data.html_student_type_list);
                    $("#modal-student_type").modal("hide");
                } else {
                    $("#modal-student_type .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create student_type
    $(".js-create-student_type").click(loadForm);
    $("#modal-student_type").on("submit", ".js-student_type-create-form", saveForm);

     // view student_type
     $("#student_type-table").on("click", ".js-view-student_type", loadForm);
    $("#modal-student_type").on("submit", ".js-student_type-view-form", saveForm);

    // Update student_type
    $("#student_type-table").on("click", ".js-update-student_type", loadForm);
    $("#modal-student_type").on("submit", ".js-student_type-update-form", saveForm);

    // Delete student_type
    $("#student_type-table").on("click", ".js-delete-student_type", loadForm);
    $("#modal-student_type").on("submit", ".js-student_type-delete-form", saveForm);

});