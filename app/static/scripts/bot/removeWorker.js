function removeWorker(idx) {
    $.ajax({
        data: {"remove_worker": idx, "section": "employee"},
        type: "GET",
        url: "",
        success: function(result){
            $("#main").html(result);
        }
    });

    }