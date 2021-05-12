$(function() {
    console.log("Search Component!");
    
    updateData();
    
    var docsTable = $("#docsTable");
    var modalContainer = $("#modalContainer");
    var addBtn = $("#addBtn");
    var searchBtn = $("#searchBtn");

    addBtn.on("click", function(){
        openModal(modalContainer, "/modal", "Adicionar Documento", "/create-document");
    });

    docsTable.on('click', 'tbody tr', function() {
        let current = $(this);
        let name = current.find("td").eq(0).html();
        openModal(modalContainer, "/modal", `${name}`, "/manage-document");
    });
});


function updateData(){
    $.ajax({
        type : 'GET',
        url : '/document/get-pfc',
        success : function (response) {
            let documents = JSON.parse(response);
            var tableBody = $("#tableBody");
            tableBody.empty();
            for (let document of documents){
                tableBody.append(renderElement(document['nome'], document['data']));
            }
        },
        error : function (err) {
            console.log(err)
        }
    })
}

function renderElement(name, date){  
   return `
    <tr>
            <td>${name}</td>
            <td>${date}</td>
    </tr>
   `
}