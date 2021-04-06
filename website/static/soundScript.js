//alert('connect');

function playSound(name){
    
    var audio = new Audio("static/sounds/" + name + ".mp3");
    audio.play();
    setTimeout(function(){ console.log('wait 3000')}, 3000);
    
}

function clickedSound(){
    console.log('func cliked worked...');
    // console.log(window.location.href);
    // var audio = new Audio("static/sounds/clicked.mp3");
    // audio.play();
    playSound("clicked");
}

function logInSound(){
    console.log('login');
    playSound("logIn");
}


function logOutSound(){
    console.log('logout');
    playSound("logOut");
}

function nextSound(){
    console.log('next');
    playSound("next");
    
}

function wrongSound(){
    console.log('wrong');
    playSound("wrong");
}