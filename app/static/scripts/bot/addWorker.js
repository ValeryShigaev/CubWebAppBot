$('#addWorkerForm').submit(function () {
    $.ajax({
        data: $(this).serialize(),
        type: $(this).attr('method'),
        url: "{% url 'management/bot' %}",
        success: function(result){
            $("#main").html(result);
    }
    });
})