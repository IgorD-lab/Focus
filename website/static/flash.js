// Get all the flash message elements
const flashMessages = document.querySelectorAll(".flash-messages li");

// Hide each flash message after 3 seconds
flashMessages.forEach((message) => {
  setTimeout(() => {
    message.style.display = "none";
  }, 3000);
});
