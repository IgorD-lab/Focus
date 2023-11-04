var flashMessages = document.querySelectorAll(".alert");

// Loop through each flash message
flashMessages.forEach(function (message) {
  // Set the timeout duration to 3000 milliseconds (3 seconds)
  var duration = 3000;

  // Fade out the flash message after the specified duration
  setTimeout(function () {
    message.style.opacity = 0;
  }, duration);
});
