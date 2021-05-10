var server = "http://127.0.0.1:5000";
var modalContainer = $("#modalContainer");

$( function() {
  $("#registerForm").submit(function(e) {
    e.preventDefault();
  })

  $("#submitUser").click(function(e) {
        var appdir='/auth/register';

        var userJSON = {
          "nome": $("#nome").val(),
          "sobrenome": $("#sobrenome").val(),
          "nascimento": $("#nascimento").val(),
          "login": $("#login").val(),
          "senha": $("#senha").val()
        }
        console.log(userJSON);
        $.ajax({
            type: "POST",
            url:server+appdir,
            data: JSON.stringify(userJSON),
            dataType: 'json'
        }).done(function(data) { 
          console.log(data);
          console.log(e);
          setTimeout(() => {
            modalContainer.modal("hide");
          },2000);
        });
  });
});