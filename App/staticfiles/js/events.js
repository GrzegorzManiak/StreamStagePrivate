// Function for like button

const like_buttons = document.querySelectorAll('.like-button');
like_buttons.forEach(button => {

  let numberOfLikes = Number(button.getAttribute('data-likes'));
  let reviewID = button.getAttribute("data-id");
  let isLiked = button.getAttribute("user-liked").trim() == "true";

  const likeClick = () => {
    // if the like button hasn't been clicked
    if (!isLiked) {
      button.classList.add('isLiked');
      numberOfLikes++;
      isLiked = !isLiked;
    }
    // if the like button has been clicked
    else {
      button.classList.remove('isLiked');
      numberOfLikes--;
      isLiked = !isLiked;
    }
    const request = new Request("/review/" + reviewID + "/like");
    fetch(request);
    button.innerHTML='<i class="fa fa-thumbs-o-up" aria-hidden="true">&nbsp;' + numberOfLikes + '</i>';
  };
  button.addEventListener('click', likeClick);
})


// Media & Search Results/Event Listings Review Carousels
const media_settings = {
  slidesPerView: 1,
  loop: true,
  pagination: {
    el: '.swiper-pagination',
    type: 'bullets',
    clickable: 'true',
  },
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
};

const swiper = new Swiper('.mySwiper', media_settings);

// Event Page Review Carousel
const review_settings = {
  loop: true,
  slidesPerView: 2,
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
};

const long_swiper = new Swiper('.longSwiper', review_settings);

// Rating Stars
const rate = (rating) => {
  const rating_input = document.getElementById('id_rating')
  rating_input.value = rating
  
  var rs = rating_input.parentElement.parentElement.querySelector('.rating-list')
  rs.setAttribute('data-value', rating)
}

// Show More Button Function
var buttons = document.querySelectorAll(".show-more-btn")

buttons.forEach(button => {
  var id = button.getAttribute("data-showmore-id")

  var more_elem = document.querySelector(
    `.show-more-elem[data-showmore-id="${id}"]`
  )
  var less_elem = document.querySelector(
    `.show-less-elem[data-showmore-id="${id}"]`
  )

  more_elem.style.display = "none"

  button.addEventListener("click", event => {
    var visible = more_elem.style.display != "none";
    console.log( more_elem.style.display != "none")

    if (visible) {
      button.innerHTML = "Show More";
      more_elem.style.display = "none"
      less_elem.style.display = "inherit"
    } else {
        button.innerHTML = "Show Less";
      more_elem.style.display = "inherit"
      less_elem.style.display = "none"
    }
  })
})