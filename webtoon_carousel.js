const slides = document.querySelectorAll('.slide');
const nextButton = document.getElementById('next');
const prevButton = document.getElementById('prev');

let currentIndex = 0;

function updateCarousel() {
    const offset = -currentIndex * window.innerHeight; 
    document.querySelector('ul').style.transform = `translateY(${offset}px)`;

    // Hide prev button if at the first slide, otherwise show it
    if (currentIndex === 0) {
        prevButton.style.display = 'none';
    } else {
        prevButton.style.display = 'block';
    }

    // Hide next button if at the last slide, otherwise show it
    if (currentIndex === slides.length - 1) {
        nextButton.style.display = 'none';
    } else {
        nextButton.style.display = 'block';
    }
}

nextButton.addEventListener('click', () => {
    if (currentIndex < slides.length - 1) {
        currentIndex++;
        updateCarousel();
    }
});

prevButton.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
        updateCarousel();
    }
});

// script.js
function setDynamicHeight() {
    const vh = window.innerHeight * 0.01; // Calculate 1vh in pixels
    document.documentElement.style.setProperty('--vh', `${vh}px`); // Set CSS variable
}

window.addEventListener('resize', setDynamicHeight); // Update on resize
window.addEventListener('orientationchange', setDynamicHeight); // Update on orientation change

// Initial setting
setDynamicHeight();

// Initialize the carousel state
updateCarousel();
