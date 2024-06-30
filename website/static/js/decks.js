document.addEventListener('DOMContentLoaded', function() {
    const flashcards = document.querySelectorAll('[data-question-id]');
    let currentCard = 0;
    let score = 0;

    function resetQuiz() {
        currentCard = 0;
        score = 0;
        document.getElementById('completion-message').style.display = 'none';
        document.getElementById('quiz-container').style.display = 'block';
        showCard(0);
    }

    function showCard(index) {
        flashcards.forEach((card, idx) => {
            card.style.display = idx === index ? 'block' : 'none';
        });
        updateScoreDisplay();
    }

    function updateScoreDisplay() {
        document.getElementById('score').textContent = 'Score: ' + score;
    }

    flashcards.forEach((card, index) => {
        const buttons = card.querySelectorAll('button');
        const answer = card.children[2]; // Assuming the answer <p> is the third child

        buttons[0].addEventListener('click', () => { // Correct button\
            score++;
            showNextCard();
        });

        buttons[1].addEventListener('click', () => { // Incorrect button
            showNextCard();
        });
    });

    function showNextCard() {
        if (currentCard < flashcards.length - 1) {
            currentCard++;
            showCard(currentCard);
        } else {
            document.getElementById('completion-message').style.display = 'block';
            document.getElementById('quiz-container').style.display = 'none';
            document.getElementById('restart-quiz-btn').style.display = 'block'; // Show the restart button
            document.getElementById('score').textContent = `Final Score: ${score}/${flashcards.length}`;
        }
    }

    document.getElementById('restart-quiz-btn').addEventListener('click', function() {
        window.history.back(); // Go back to the previous page
    });

    resetQuiz(); // Initialize the quiz
});
