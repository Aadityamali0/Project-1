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
            slidesPerView: 1.8, 
            spaceBetween: 10
        },
        468: {
            slidesPerView: 2.3,
            spaceBetween: 10
        },
        // Tablet Layout
        768: {
            slidesPerView: 3,
            spaceBetween: 15
        },
        // Desktop Layout
        1080: {
            slidesPerView: 3.7, 
            spaceBetween: 30
        }
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    }
});
