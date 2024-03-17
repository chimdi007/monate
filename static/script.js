const navMenu=document.querySelector('.off-screen-menu');


const hamMenu=document.querySelector('.ham-menu');


hamMenu.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    offScreenMenu.classList.toggle('active');
})