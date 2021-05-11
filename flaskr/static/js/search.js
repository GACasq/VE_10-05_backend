$(function() {
    console.log("Search Component!");
    
    var docsTable = $("#docsTable");
    var modalContainer = $("#modalContainer");
    var addBtn = $("#addBtn");
    var searchBtn = $("#searchBtn");

    if(!checkAuth()){
        addBtn.hide();
    }

    addBtn.on("click", function(){
        openModal(modalContainer, "/modal", "Adicionar Documento", "/create-document");
    });

    docsTable.on('click', 'tbody tr', function() {
        let current = $(this);
        let name = current.find("td").eq(0).html();
        openModal(modalContainer, "/modal", `${name}`, "/manage-document");
    });
});