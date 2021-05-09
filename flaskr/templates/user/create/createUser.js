function myFunction(e) {
  //FIRST WE CAPTURE THE VALUE THAT THE USER INPUTS
  let userInput = {toSend: e.currentTarget.previousElementSibling.value}
  let userInput2 = e.
  //THEN WE SEND IT TO THE FLASK BACKEND USING AJAX (Fetch API)
  fetch("/api/path/to/flask/route", {
    method: 'POST',
    headers: {
     "Content-Type": "application/json",
    },
    body: JSON.stringify(userInput)
  }
  )
}
/*
$( "#submitUser" ).submit(function( event ) {
  alert( "Handler for .submit() called." );
  console.log("deu certo entrar");
  event.preventDefault();
});*/
  
var server = "http://127.0.0.1:5000";
var modalContainer = $("#modalContainer");

$( function() {
  $("#registerForm").submit(function(e) {
    e.preventDefault();
    modalContainer.modal("hide");
  })

  $("#submitUser").click(function(e) {
        var appdir='/auth/register';

        var userJSON = {
          "username": $("#login").val(),
          "first_name": $("#nome").val(),
          "last_name": $("#sobrenome").val(),
          "birth_date": $("#nascimento").val(),
          "password": $("#senha").val()
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
          console.log(modalContainer.modal("hide"));
        });
  });
});