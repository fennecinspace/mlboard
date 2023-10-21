// document.addEventListener('click', (event) => {
//     var lng_picker = document.querySelector('#lng_picker > div > a');
//     if (lng_picker && event.target != lng_picker && lng_picker.hasAttribute('opened')){
//         lng_picker.removeAttribute('opened');
//         document.querySelector('#language_picker').style.display = 'none';
//     }

//     var edition_selector = document.querySelector('#edition_selector > div');
//     if (edition_selector && event.target != edition_selector && edition_selector.hasAttribute('opened')){
//         edition_selector.removeAttribute('opened');
//         document.querySelector('#edition_picker').style.display = 'none';
//     }
// });

// document.querySelector('#lng_picker > div > a').addEventListener('click', function () {
//     if (this.hasAttribute('opened')) {
//         document.querySelector('#language_picker').style.display = 'none';
//         this.removeAttribute('opened');
//     }
//     else {
//         document.querySelector('#language_picker').style.display = 'grid';
//         this.setAttribute('opened', '');
//     }
// });

document.querySelector('.hamburger').addEventListener('click', function () {
    if (this.classList.contains('is-active')) {
        document.querySelector('.hamburger').classList.remove('is-active');
        document.querySelector('nav').style.display = "none"; 
        document.querySelector('#navbar_special_btns').style.display = "grid"; 
        document.querySelector('#edition_selector').style.display = "grid"; 
        
    }
    else {
        document.querySelector('.hamburger').classList.add('is-active');
        document.querySelector('nav').style.display = "grid"; 
        document.querySelector('#navbar_special_btns').style.display = "none"; 
        document.querySelector('#edition_selector').style.display = "none"; 
    }
});