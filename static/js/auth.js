document.addEventListener('DOMContentLoaded', function() {
    // Password strength visualization for registration form
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            validatePassword(this.value);
        });
    }
    
    // Password confirmation match check
    const confirmPasswordInput = document.getElementById('confirm_password');
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', function() {
            checkPasswordMatch(passwordInput.value, this.value);
        });
    }
});

function validatePassword(password) {
    // Create password strength indicator if it doesn't exist
    let strengthIndicator = document.getElementById('password-strength');
    if (!strengthIndicator) {
        const passwordField = document.getElementById('password').parentNode;
        strengthIndicator = document.createElement('div');
        strengthIndicator.id = 'password-strength';
        strengthIndicator.className = 'progress mt-2';
        strengthIndicator.innerHTML = '<div class="progress-bar" role="progressbar" style="width: 0%"></div>';
        passwordField.appendChild(strengthIndicator);
    }
    
    // Get the progress bar
    const progressBar = strengthIndicator.querySelector('.progress-bar');
    
    // Calculate password strength
    let strength = 0;
    
    // Check length
    if (password.length >= 8) strength += 25;
    
    // Check for uppercase letters
    if (/[A-Z]/.test(password)) strength += 25;
    
    // Check for lowercase letters
    if (/[a-z]/.test(password)) strength += 25;
    
    // Check for numbers
    if (/[0-9]/.test(password)) strength += 25;
    
    // Update progress bar
    progressBar.style.width = strength + '%';
    
    // Set color based on strength
    if (strength < 50) {
        progressBar.className = 'progress-bar bg-danger';
    } else if (strength < 75) {
        progressBar.className = 'progress-bar bg-warning';
    } else {
        progressBar.className = 'progress-bar bg-success';
    }
}

function checkPasswordMatch(password, confirmPassword) {
    const confirmField = document.getElementById('confirm_password').parentNode;
    let matchIndicator = document.getElementById('password-match');
    
    if (!matchIndicator) {
        matchIndicator = document.createElement('div');
        matchIndicator.id = 'password-match';
        matchIndicator.className = 'text-danger mt-1';
        confirmField.appendChild(matchIndicator);
    }
    
    if (password === confirmPassword) {
        matchIndicator.className = 'text-success mt-1';
        matchIndicator.innerHTML = '<i class="bi bi-check-circle"></i> Passwords match';
    } else {
        matchIndicator.className = 'text-danger mt-1';
        matchIndicator.innerHTML = '<i class="bi bi-x-circle"></i> Passwords do not match';
    }
}
