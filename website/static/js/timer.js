// Define the timer and the interval
let timer = 25 * 60;
let interval;
let selectedTime = 25 * 60; // Default selected time
let isRunning = false;

// Get the buttons and the timer display
const startButton = document.getElementById("pomodoro-start");
const stopButton = document.getElementById("pomodoro-stop");
const timerDisplay = document.getElementById("pomodoro-timer");
const timerButtons = Array.from(document.querySelectorAll(".form-check-input"));

// Update the timer display
function updateDisplay() {
  const minutes = Math.floor(timer / 60);
  const seconds = timer % 60;
  timerDisplay.textContent = `${minutes.toString().padStart(2, "0")}:${seconds
    .toString()
    .padStart(2, "0")}`;
}

// Start the timer
function startTimer() {
  isRunning = true;
  interval = setInterval(() => {
    timer--;
    updateDisplay();
    if (timer <= 0) {
      stopTimer();
    }
  }, 1000);
}

// Pause the timer
function pauseTimer() {
  isRunning = false;
  clearInterval(interval);
}

// Stop the timer
function stopTimer() {
  pauseTimer();
  timer = selectedTime; // Reset the timer to the currently selected time
  updateDisplay();
  startButton.textContent = "start"; // Reset the start button text
}

// Reset the timer
function resetTimer(newTime) {
  timer = newTime;
  selectedTime = newTime; // Update the currently selected time
  updateDisplay();
  startButton.textContent = "start"; // Reset the start button text
  pauseTimer();
}

// Event listeners for the buttons
startButton.addEventListener("click", () => {
  const playIcon = document.getElementById("play-icon");
  const pauseIcon = document.getElementById("pause-icon");

  if (!isRunning) {
    playIcon.classList.add("hidden");
    pauseIcon.classList.remove("hidden");
    startTimer();
  } else {
    playIcon.classList.remove("hidden");
    pauseIcon.classList.add("hidden");
    pauseTimer();
  }
});

stopButton.addEventListener("click", () => {
  stopTimer();
});

timerButtons.forEach((button) => {
  button.addEventListener("change", () => {
    switch (button.value) {
      case "pomodoro":
        resetTimer(25 * 60);
        break;
      case "short":
        resetTimer(5 * 60);
        break;
      case "long":
        resetTimer(10 * 60);
        break;
    }
  });
});

// Initialize the display
updateDisplay();
