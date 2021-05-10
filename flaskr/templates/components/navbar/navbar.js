$(function() {
    console.log("Navbar Component!");
    var modalContainer = $("#modalContainer");
    var loginForm = $("#loginForm");
    var logoutBtn = $("#logoutBtn");
    var addUserBtn = $("#addUserBtn");
    var userOptions = $("#userOptions");

    if(checkAuth()){
        loginForm.removeClass("d-flex");
        loginForm.hide();

        userOptions.removeClass("d-none");
    };
    
    //$("loginButton").click(function(e){
    loginForm.submit(function(e){
        e.preventDefault();
        console.log("depois do prevent");
        if($("#loginInput").val() && $("#passwordInput").val()){
            var server = "http://127.0.0.1:5000";
            var appdir='/auth/login';
            console.log("chegou aqui");
            var userJSON = {
                "login": $("#loginInput").val(),
                "senha": $("#passwordInput").val()
              }

            $.ajax({
                type: "POST",
                url:server+appdir,
                data: JSON.stringify(userJSON),
                success: function (response) {
                    console.log(response);
                    console.log("fora do sucess");
                    if(response=="true"){
                        console.log("dentro do sucess");
                        setCookie($("#loginInput").val() && $("#passwordInput").val());
                        location.reload();
                    }
                },
                dataType: 'json'
            })
        };
    });
    /*
    $("loginButton").click(function(e){
    //loginForm.submit(function(e){

        $("#loginForm").submit(function(e) {
            e.preventDefault();
          })

        if($("#loginInput").val() && $("#passwordInput").val()){
            setCookie($("#loginInput").val() && $("#passwordInput").val());
            location.reload();
        };
    });*/


    logoutBtn.on("click", function(){
        setCookie(false);
        location.reload();
    });

    addUserBtn.on("click", function(){
        openModal(modalContainer, "components/modal/modal.html", "Cadastrar Usuário", "user/create/createUser.html");
    });
});