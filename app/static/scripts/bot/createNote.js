$('#addNoteForm').submit(function () {
    alert("hi")
    $.ajax({
        data: $(this).serialize(),
        type: $(this).attr('method'),
        url: "{% url 'management/bot' %}",
        success: function(result){
            $("#main").html(result);
    }
    });
})