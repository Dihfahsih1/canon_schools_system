$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-ebook").modal("show");
            },
            success: function (data) {
                $("#modal-ebook .modal-content").html(data.html_form);
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
                    $("#ebook-table tbody").html(data.html_book_list);
                    $("#modal-ebook").modal("hide");
                } else {
                    $("#modal-ebook .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */

    // Create ebook
    $(".js-create-ebook").click(loadForm);
    $("#modal-ebook").on("submit", ".js-ebook-create-form", saveForm);

     // view ebook
     $("#ebook-table").on("click", ".js-view-ebook", loadForm);
    $("#modal-ebook").on("submit", ".js-ebook-view-form", saveForm);

    // Update ebook
    $("#ebook-table").on("click", ".js-update-ebook", loadForm);
    $("#modal-ebook").on("submit", ".js-ebook-update-form", saveForm);

    // Delete ebook
    $("#ebook-table").on("click", ".js-delete-ebook", loadForm);
    $("#modal-ebook").on("submit", ".js-ebook-delete-form", saveForm);

});