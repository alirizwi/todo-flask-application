$.fn.submitViaAjax = function (success, error) {
    this.on('submit', function (e) {
        e.preventDefault();
        var form = this;
        $.ajax({
            method: form.method,
            url: form.action,
            data: $(form).serialize(),
            success: success ? success.bind(form) : function () {},
            error: error? error.bind(form) : function () {},
        });
        return false;
    });
    return this;
};
