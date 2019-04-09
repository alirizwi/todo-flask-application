var todoManager = (function () {
    var markDone = function() {
        id = $(this).data('id');
        $.ajax({
            method: 'post',
            url: '/api/todo/' + id + '/done',
            success: function(res) {
                listAll();
            }
        })
    }

    var deleteTask = function() {
        id = $(this).data('id');
        $.ajax({
            method: 'post',
            url: '/api/todo/' + id + '/delete',
            success: function(res) {
                listAll();
            }
        })
    }

    var listAll = function () {
        $.ajax({
            method: 'get',
            url: '/api/todo',
            success: function(res) {
                console.log(res.todos);
                viewManager.render('todos-list', {
                    todos: res.todos,
                }, function($view) {
                    $view.find(".mark-as-done").click(markDone);
                    $view.find(".delete-task").click(deleteTask);
                });
            }
        });
    };

    var create = function () {
        viewManager.render('todo', {
            formAction: '/api/todo',
        }, function ($view) {
            console.log($view);
            $view.submitViaAjax(function (response) {
                page('/');
            });
        });
    };

    var listOne = function (id) {
        $.ajax({
            method: 'get',
            url: '/api/todo',
            success: function(res) {
                console.log(res.todos[0]);
                viewManager.render('todo', res.todos[0]);
            }
        })
    };

    var tManager = {};
    tManager.listAll = listAll;
    tManager.listOne = listOne;
    tManager.create = create;
    return tManager;
})();
