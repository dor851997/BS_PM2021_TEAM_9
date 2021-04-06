//alert('connect');

function playSound(name){
    
    var audio = new Audio("static/sounds/" + name + ".mp3");
    audio.play();
    
}

function clickedSound(){
    // console.log('func cliked worked...');
    // console.log(window.location.href);
    // var audio = new Audio("static/sounds/clicked.mp3");
    // audio.play();
    playSound("clicked");
}

function logInSound(){
    playSound("logIn");
}


function logOutSound(){
    playSound("logOut");
}

function nextSound(){
    playSound("next");
}

function wrongSound(){
    playSound("wrong");
}