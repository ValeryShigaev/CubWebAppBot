function removeObject(idx) {
    $.ajax({
        data: {"remove_object": idx, "section": "objects"},
        type: "GET",
        url: "",
        success: function(result){
            $("#main").html(result);
        }
    });

    }