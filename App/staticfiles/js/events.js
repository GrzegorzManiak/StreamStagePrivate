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
    const request = new Request("/events/review/" + reviewID + "/like");
    fetch(request);
    button.innerHTML='<i class="fa fa-thumbs-o-up" aria-hidden="true">&nbsp;' + numberOfLikes + '</i>';
  };
  button.addEventListener('click', likeClick);
})

