$(function() {
    console.log("Navbar Component!");
    var modalContainer = $("#modalContainer");
    var logoutBtn = $("#logoutBtn");
    var addUserBtn = $("#addUserBtn");

    logoutBtn.on("click", function(){
        console.log("Logout")
        $.ajax({
            type: "GET",
            url: "/auth/logout",
            success: () => location.reload()
        })
    });

    addUserBtn.on("click", function(){
        openModal(modalContainer, "/modal", "Cadastrar Usuário", "/create-user");
    });
});