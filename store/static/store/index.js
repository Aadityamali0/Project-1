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

/* ---------------------------------------------------------------
   Blurred backdrop that echoes the active slide's photo.
   Two absolutely-positioned layers (#swiperBg1 / #swiperBg2) sit
   behind the slider; whichever one is currently hidden gets the
   next image loaded into it, then we fade it in and fade the old
   one out - a simple two-layer crossfade instead of an instant swap.
   --------------------------------------------------------------- */
(function () {
    var bgLayers = [
        document.getElementById("swiperBg1"),
        document.getElementById("swiperBg2")
    ];
    if (!bgLayers[0] || !bgLayers[1]) return;

    var activeLayer = 0;

    function setBackdrop() {
        var activeSlide = swiper.slides[swiper.activeIndex];
        if (!activeSlide) return;
        var img = activeSlide.querySelector("img");
        if (!img || !img.src) return;

        var nextLayer = activeLayer === 0 ? 1 : 0;
        bgLayers[nextLayer].style.backgroundImage = "url('" + img.src + "')";
        bgLayers[nextLayer].classList.add("is-active");
        bgLayers[activeLayer].classList.remove("is-active");
        activeLayer = nextLayer;
    }

    swiper.on("slideChange", setBackdrop);
    setBackdrop(); // set the initial backdrop for the first active slide
})();
