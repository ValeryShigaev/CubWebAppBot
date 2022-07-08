function removeNote(idx) {
    $.ajax({
        data: {"remove_note": idx, "section": "my_notes", "tg_idx": GetIdx},
        type: "GET",
        url: "",
        success: function(result){
            $("#main").html(result);
        }
    });

    }