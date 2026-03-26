/**
 * Auth Form Enhancement - Login & Registration
 * Provides form validation, animations, and UX improvements
 */

document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.auth-card form');
    
    forms.forEach(form => {
        initializeFormValidation(form);
        setupInputAnimations(form);
        setupPasswordVisibility(form);
        setupFormSubmit(form);
    });
});

/**
 * Initialize form validation with visual feedback
 */
function initializeFormValidation(form) {
    const inputs = form.querySelectorAll('.form-control');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                validateField(this);
            }
        });
    });
}

/**
 * Validate individual field
 */
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.getAttribute('name');
    const fieldType = field.getAttribute('type');
    
    // Clear previous error state
    field.classList.remove('is-invalid', 'is-valid');
    
    // Skip validation for empty optional fields
    if (value === '' && !field.required) {
        return true;
    }
    
    // Check if field is empty (required)
    if (value === '') {
        markFieldInvalid(field, 'This field is required');
        return false;
    }
    
    // Field-specific validation
    let isValid = true;
    
    if (fieldType === 'email') {
        isValid = validateEmail(value);
        if (!isValid) {
            markFieldInvalid(field, 'Please enter a valid email address');
        }
    } else if (fieldName === 'password1' || fieldName === 'password') {
        isValid = value.length >= 8;
        if (!isValid) {
            markFieldInvalid(field, 'Password must be at least 8 characters');
        }
    } else if (fieldName === 'password2') {
        const password1 = form.querySelector('[name="password1"]');
        if (password1 && password1.value !== value) {
            markFieldInvalid(field, 'Passwords do not match');
            return false;
        }
    } else if (fieldName === 'username') {
        isValid = /^[a-zA-Z0-9_-]{3,}$/.test(value);
        if (!isValid) {
            markFieldInvalid(field, 'Username must be 3+ characters (letters, numbers, _, -)');
        }
    }
    
    if (isValid) {
        field.classList.add('is-valid');
    }
    
    return isValid;
}

/**
 * Mark field as invalid with message
 */
function markFieldInvalid(field, message) {
    field.classList.add('is-invalid');
    
    // Remove old error message if exists
    const oldError = field.parentElement.querySelector('.invalid-feedback');
    if (oldError) {
        oldError.remove();
    }
    
    // Add new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.textContent = message;
    errorDiv.style.color = '#c33';
    errorDiv.style.fontSize = '12px';
    errorDiv.style.marginTop = '4px';
    field.parentElement.appendChild(errorDiv);
}

/**
 * Email validation
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Setup input focus animations
 */
function setupInputAnimations(form) {
    const inputs = form.querySelectorAll('.form-control');
    
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (this.value === '') {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // Mark as focused if already has value
        if (input.value !== '') {
            input.parentElement.classList.add('focused');
        }
    });
}

/**
 * Setup password visibility toggle
 */
function setupPasswordVisibility(form) {
    const passwordFields = form.querySelectorAll('input[type="password"]');
    
    passwordFields.forEach((field, index) => {
        // Create wrapper
        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        field.parentElement.insertBefore(wrapper, field);
        wrapper.appendChild(field);
        
        // Create toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.className = 'password-toggle';
        toggleBtn.innerHTML = '<i class="fa fa-eye"></i>';
        toggleBtn.style.cssText = `
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: #7f8c8d;
            cursor: pointer;
            padding: 5px;
            font-size: 16px;
            z-index: 10;
        `;
        
        wrapper.appendChild(toggleBtn);
        
        toggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const isPassword = field.type === 'password';
            field.type = isPassword ? 'text' : 'password';
            toggleBtn.innerHTML = isPassword ? '<i class="fa fa-eye-slash"></i>' : '<i class="fa fa-eye"></i>';
            toggleBtn.style.color = isPassword ? '#b0b435' : '#7f8c8d';
        });
    });
}

/**
 * Setup form submit with validation
 */
function setupFormSubmit(form) {
    form.addEventListener('submit', function(e) {
        const inputs = this.querySelectorAll('.form-control');
        let isFormValid = true;
        
        inputs.forEach(input => {
            if (!validateField(input)) {
                isFormValid = false;
            }
        });
        
        if (!isFormValid) {
            e.preventDefault();
            showFormError(this, 'Please fix the errors above');
        }
    });
}

/**
 * Show form-level error message
 */
function showFormError(form, message) {
    const existing = form.querySelector('.form-error-message');
    if (existing) {
        existing.remove();
    }
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error-message alert alert-danger';
    errorDiv.innerHTML = `<i class="fa fa-exclamation-circle"></i> ${message}`;
    errorDiv.style.cssText = `
        background: #fee;
        color: #c33;
        padding: 12px 15px;
        border-radius: 6px;
        border-left: 4px solid #c33;
        margin-bottom: 20px;
        animation: slideDown 0.3s ease-out;
    `;
    
    form.insertBefore(errorDiv, form.firstChild);
}

/**
 * Password strength indicator (optional enhancement)
 */
function setupPasswordStrength(form) {
    const passwordField = form.querySelector('input[name="password1"]');
    if (!passwordField) return;
    
    const indicator = document.createElement('div');
    indicator.className = 'password-strength';
    indicator.style.cssText = `
        height: 4px;
        background: #e9ecef;
        border-radius: 2px;
        margin-top: 8px;
        overflow: hidden;
    `;
    
    const bar = document.createElement('div');
    bar.style.cssText = `
        height: 100%;
        width: 0%;
        background: #dc3545;
        transition: all 0.3s ease;
    `;
    indicator.appendChild(bar);
    passwordField.parentElement.appendChild(indicator);
    
    passwordField.addEventListener('input', function() {
        const strength = calculatePasswordStrength(this.value);
        const colors = ['#dc3545', '#fd7e14', '#ffc107', '#17a2b8', '#28a745'];
        const widths = ['20%', '40%', '60%', '80%', '100%'];
        
        bar.style.width = widths[strength];
        bar.style.background = colors[strength];
    });
}

/**
 * Calculate password strength (0-4 scale)
 */
function calculatePasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[!@#$%^&*]/.test(password)) strength++;
    
    return Math.min(strength - 1, 4);
}

// Add slide down animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);
