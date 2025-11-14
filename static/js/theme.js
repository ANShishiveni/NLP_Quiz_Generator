document.addEventListener('DOMContentLoaded', function() {
    // Get the theme toggle button
    const themeToggle = document.getElementById('themeToggle');
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            toggleTheme();
        });
    }
    
    // Apply stored theme on page load (if any)
    applyStoredTheme();
});

function toggleTheme() {
    // Make AJAX request to toggle theme on server
    fetch('/toggle-theme', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Update the HTML element with the new theme
        document.documentElement.setAttribute('data-bs-theme', data.theme);
        
        // Update the toggle button icon
        updateThemeIcon(data.theme);
    })
    .catch(error => {
        console.error('Error toggling theme:', error);
    });
}

function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        if (theme === 'light') {
            themeToggle.innerHTML = '<i class="bi bi-moon"></i>';
        } else {
            themeToggle.innerHTML = '<i class="bi bi-sun"></i>';
        }
    }
}

function applyStoredTheme() {
    // The theme is set server-side in the base.html template
    // This function can be used for additional client-side theme adjustments if needed
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    updateThemeIcon(currentTheme);
}
