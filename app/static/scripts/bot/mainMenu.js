
try{
    let tg = window.Telegram.WebApp;
    let idx = tg.initDataUnsafe.user.id
    //tg.MainButton.setText("Select it");
    //tg.MainButton.show();
    function GetIdx(){
    return idx;
}

}catch(error){
    if(error.name == 'TypeError'){
        document.getElementById('warn').classList.add('bot_show')
        document.getElementById('main').remove()
        
    }
}



    

