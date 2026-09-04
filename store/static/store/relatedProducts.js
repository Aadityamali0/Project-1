new Swiper('.card-wrapper', {
  // loop: true,

  // If we need pagination
//   pagination: {
//     el: '.swiper-pagination',
//   },

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  breakpoints: {
    0: {
        slidesPerView: 3.5
    },
    768: {
        slidesPerView: 3.5
    },
    1024: {
        slidesPerView: 4.5
    },
  }
});