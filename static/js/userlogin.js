$(document).ready(function() {
    function chesum_login() {

        var $login_username = $("#login_username").val();
        var $login_password = $("#login_password").val();

        var userobj = {};
        userobj.login_username = $login_username;
        userobj.login_password = $login_password;

        if ($login_username && $login_password) {
            $.post("/login/", JSON.stringify(userobj), function(data) {
                if (data['status'] == "ok") {
                    location.href = '/base/';
                } else {
                    swal(data['msg']);
                }
            });
        }

    }
    $("#user_loginbtn").click(function() {
        chesum_login();
    });

    $('#login_password').bind('keypress', function(event) {
        if (event.keyCode == "13") {
            chesum_login();
        }
    });


//用户退出js

    $("#logoutjs").click(function() {
        var get_loginuser = $("#get_loginuser").text();
        var data = {};
        data.user = get_loginuser;
    
        if (get_loginuser) {
            $.post('/logout/', JSON.stringify(data),
            function(result) {
                if (result['status'] === 'ok') {
    
                    window.location = "/login/"
                };
            })
        }
    });


})

