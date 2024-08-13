//navbar

const navMenu = document.getElementById('nav-menu')
      navToggle = document.getElementById('toogle')
      navClose = document.getElementById('close-tag')

if(navToggle){
    navToggle.addEventListener('click',() =>{
        navMenu.classList.add('show-menu')
    })
}

if (navClose) {
    navClose.addEventListener('click', () =>{
        navMenu.classList.remove('show-menu')
    })
}


const navLink = document.querySelectorAll('nav-link')
const linkAction = () =>{
    const navMenu = document.getElementById('nav-menu')
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click',linkAction))

const blurHeader = () =>{
    const header = document.getElementById('header')
    this.scrollY >= 50 ? header.classList.add('blur-header')
                       : header.classList.remove('blur-header')
}
window.addEventListener('scroll',blurHeader)



//popupmessage

document.addEventListener('DOMContentLoaded', function() {
    const popupMessage = document.getElementById('popupMessage');
    const popupText = document.getElementById('popupText');
    const closePopup = document.getElementById('closePopup');

    // Check if there are messages in the page
    if (document.getElementById('messageContent')) {
        const messageContent = document.getElementById('messageContent').textContent;
        popupText.textContent = messageContent;
        popupMessage.style.display = 'flex';
    }

    closePopup.addEventListener('click', function() {
        popupMessage.style.display = 'none';
    });

    // Optional: Automatically hide the popup after a few seconds
    setTimeout(() => {
        popupMessage.style.display = 'none';
    }, 5000); // Adjust the duration as needed
});
