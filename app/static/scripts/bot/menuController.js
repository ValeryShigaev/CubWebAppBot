function turnMenu(section) {
    $.ajax({
        data: {"section": section, "tg_idx": GetIdx},
        type: "GET",
        url: "",
        success: function(result){
            $("#main").html(result);
        }
    });

    }