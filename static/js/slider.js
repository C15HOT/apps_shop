const slider = document.querySelector(".slider-container");
const nextBtn = document.querySelector(".next-btn");
const prevBtn = document.querySelector(".prev-btn");
const slides = document.querySelectorAll(".slide-container");
const slideIcon = document.querySelectorAll(".slide-icon");
const numberOfSlides = slides.length;
var slideNumber = 0;
slides[0].classList.add("active");
slideIcon[0].classList.add("active");

// Image slider next button
nextBtn.addEventListener("click", () => {
    slides.forEach((slide) => {
        slide.classList.remove("active");
    });
    slideIcon.forEach((slideIcon) => {
        slideIcon.classList.remove("active");
    });

    slideNumber++;

    if(slideNumber > (numberOfSlides - 1)){
        slideNumber = 0;
    }

    slides[slideNumber].classList.add("active");
    slideIcon[slideNumber].classList.add("active");
});

// Image slider prev button

prevBtn.addEventListener("click", () => {
    slides.forEach((slide) => {
        slide.classList.remove("active");
    });
    slideIcon.forEach((slideIcon) => {
        slideIcon.classList.remove("active");
    });

    slideNumber--;

    if(slideNumber < 0){
        slideNumber = numberOfSlides-1;
    }

    slides[slideNumber].classList.add("active");
    slideIcon[slideNumber].classList.add("active");
})
// Autoplay

var playSlider;
var repeater = () => {
    playSlider = setInterval(function(){
        slides.forEach((slide) => {
        slide.classList.remove("active");
    });
    slideIcon.forEach((slideIcon) => {
        slideIcon.classList.remove("active");
    });

    slideNumber++;

    if(slideNumber > (numberOfSlides - 1)){
        slideNumber = 0;
    }

    slides[slideNumber].classList.add("active");
    slideIcon[slideNumber].classList.add("active");
    }, 4000);
};
repeater();

// Stop autoplay slider
slider.addEventListener("mouseover", ()=>{
    clearInterval(playSlider);
});

// Start autoplay slider
slider.addEventListener("mouseout", () => {
    repeater();
});