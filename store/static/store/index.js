var swiper = new Swiper(".mySwiper", {
    grabCursor: true,
    centeredSlides: true,
    loop: true,    
    watchSlidesProgress: true, // Forces Swiper to calculate slide visibility correctly
    speed: 600,
    autoplay: {
        delay: 2000,
        disableOnInteraction: false,
        pauseOnMouseEnter: true
    },
    breakpoints: {
        // Mobile Layout (3 slides visible)
        0: {
            slidesPerView: 2.3, 
            spaceBetween: 10
        },
        // Tablet Layout
        768: {
            slidesPerView: 2.5,
            spaceBetween: 25
        },
        // Desktop Layout
        1200: {
            slidesPerView: 3.7, 
            spaceBetween: 40
        }
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    }
});
