$(function() {
    console.log("Search Component!");
    
    var docsTable = $("#docsTable");
    var modalContainer = $("#modalContainer");
    var addBtn = $("#addBtn");
    var searchForm = $("#searchForm");

    updateData();
    
    addBtn.on("click", function(){
        openModal(modalContainer, "/modal", "Adicionar Documento", "/create-document");
    });

    docsTable.on('click', 'tbody tr', function() {
        let current = $(this);
        let name = current.find("td").eq(0).html();
        openModal(modalContainer, "/modal", `${name}`, "/manage-document");
    });

    searchForm.submit(function(e) {
        e.preventDefault();
        searchData();
    })
});


function updateData(){
    $.ajax({
        type : 'GET',
        url : '/document/get-pfc',
        success : (response) => renderTable(JSON.parse(response)),
        error : (err) => console.log(err)
        
    })
}

function searchData(){
    let text = $("#searchInput").val();
    $.ajax({
        type : 'POST',
        url : '/document/search-pfc',
        data: {"search": text},
        dataType: 'json',
        success : (response) => renderTable(response),
        error : (err) => console.log(err)
    })
}

function renderTable(contentArray){
    var tableBody = $("#tableBody");
    tableBody.empty();
    for (let content of contentArray){
        if(content['nome']!=null && content['data']!=null){
            tableBody.append(renderElement(content['nome'], content['data']));
        }
    }
}

function renderElement(name, date){  
   return `
    <tr>
            <td>${name}</td>
            <td>${date}</td>
    </tr>
   `
}