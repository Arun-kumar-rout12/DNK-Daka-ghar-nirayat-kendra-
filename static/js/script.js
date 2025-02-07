document.addEventListener('DOMContentLoaded', function () {
    // Function to format time in HH:MM:SS
    function formatTime(seconds) {
        const hrs = Math.floor(seconds / 3600);
        const mins = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    // Set the initial timer to 1 hour (3600 seconds)
    let timeLeft = 3600;
    const countdownElement = document.getElementById('countdown');

    // Update the timer every second
    const timerInterval = setInterval(() => {
        timeLeft--;
        countdownElement.textContent = formatTime(timeLeft);

        // Check if time has run out
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            alert("Session timed out. You have been logged out due to inactivity.");
            window.location.href = "{% url 'logout' %}";  // Redirect to the logout page
        }
    }, 1000);

    // Optional: Reset the timer on user activity (mousemove or keypress)
    function resetTimer() {
        timeLeft = 3600;  // Reset to 1 hour
    }

    document.addEventListener('mousemove', resetTimer);
    document.addEventListener('keypress', resetTimer);
});
