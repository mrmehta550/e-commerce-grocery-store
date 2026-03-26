/**
 * Enhanced Navbar Top Bar Interactions
 * Provides smooth animations, dropdown enhancements, and UX improvements
 */

document.addEventListener('DOMContentLoaded', function() {
    enhanceNavbarTopBar();
    setupDropdownAnimations();
    setupLinkHoverEffects();
    setupScrollEffects();
    setupSelectPickerCustomization();
});

/**
 * Enhance navbar top bar with class manipulation
 */
function enhanceNavbarTopBar() {
    const mainTop = document.querySelector('.main-top');
    if (!mainTop) return;
    
    // Add animation class on page load
    mainTop.addEventListener('mouseenter', function() {
        this.style.boxShadow = '0 6px 16px rgba(0,0,0,0.2)';
        this.style.transition = 'box-shadow 0.3s ease';
    });
    
    mainTop.addEventListener('mouseleave', function() {
        this.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    });
}

/**
 * Setup dropdown menu animations
 */
function setupDropdownAnimations() {
    const selects = document.querySelectorAll('.login-box .selectpicker');
    
    selects.forEach(select => {
        const button = select.parentElement.querySelector('.btn');
        if (!button) return;
        
        // Create custom dropdown container
        const dropdown = select.parentElement.querySelector('.dropdown-menu');
        if (!dropdown) return;
        
        // Enhance dropdown visibility on open
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (dropdown.style.display === 'block' || dropdown.classList.contains('show')) {
                    animateDropdownIn(dropdown);
                }
            });
        });
        
        observer.observe(dropdown, {
            attributes: true,
            attributeFilter: ['style', 'class']
        });
        
        // Animate items on hover
        const items = dropdown.querySelectorAll('.dropdown-item');
        items.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.05}s`;
            item.style.animation = 'fadeInLeft 0.3s ease';
            
            item.addEventListener('mouseover', function() {
                this.style.paddingLeft = '20px';
                this.style.transition = 'padding-left 0.2s ease';
            });
            
            item.addEventListener('mouseout', function() {
                this.style.paddingLeft = '16px';
            });
        });
    });
}

/**
 * Animate dropdown entrance
 */
function animateDropdownIn(dropdown) {
    dropdown.style.animation = 'slideDownSmooth 0.3s ease-out';
    dropdown.style.opacity = '1';
}

/**
 * Setup link hover effects with ripple
 */
function setupLinkHoverEffects() {
    const ourLinks = document.querySelectorAll('.our-link ul li a');
    
    ourLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            createRipple(this);
        });
        
        // Icon animation
        const icon = this.querySelector('i');
        if (icon) {
            this.addEventListener('mouseenter', function() {
                icon.style.animation = 'iconBounce 0.4s ease';
            });
        }
    });
}

/**
 * Create ripple effect on click
 */
function createRipple(element) {
    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    ripple.style.cssText = `
        position: absolute;
        width: 20px;
        height: 20px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        pointer-events: none;
        animation: rippleEffect 0.6s ease-out;
    `;
    
    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 600);
}

/**
 * Setup scroll effects - navbar changes on scroll
 */
function setupScrollEffects() {
    const mainTop = document.querySelector('.main-top');
    if (!mainTop) return;
    
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        let currentScroll = window.pageYOffset || document.documentElement.scrollTop;
        
        if (currentScroll > 100) {
            mainTop.style.position = 'sticky';
            mainTop.style.top = '0';
            mainTop.style.zIndex = '999';
            mainTop.style.boxShadow = '0 8px 20px rgba(0,0,0,0.25)';
        } else {
            mainTop.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
        }
        
        lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
    }, false);
}

/**
 * Customize Bootstrap Select Picker appearance
 */
function setupSelectPickerCustomization() {
    const selects = document.querySelectorAll('.selectpicker');
    
    selects.forEach(select => {
        // Add custom classes
        const button = select.parentElement.querySelector('.btn');
        if (button) {
            button.classList.add('selectpicker-custom');
            
            // Smooth open/close
            button.addEventListener('click', function() {
                const menu = this.parentElement.querySelector('.dropdown-menu');
                if (menu) {
                    menu.style.transition = 'all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
                }
            });
        }
    });
}

// Inject animations into page
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDownSmooth {
        from {
            opacity: 0;
            transform: translateY(-8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInLeft {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes iconBounce {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(3px); }
    }
    
    @keyframes rippleEffect {
        0% {
            width: 20px;
            height: 20px;
            opacity: 1;
        }
        100% {
            width: 200px;
            height: 200px;
            opacity: 0;
        }
    }
    
    .our-link ul li a {
        position: relative;
    }
    
    .selectpicker-custom {
        position: relative !important;
    }
`;
document.head.appendChild(style);

// Handle dropdown item selection
document.addEventListener('click', function(e) {
    if (e.target.closest('.login-box .dropdown-item')) {
        const item = e.target.closest('.login-box .dropdown-item');
        const url = item.getAttribute('data-value') || item.getAttribute('value');
        
        if (url && url !== '#') {
            // Add loading effect
            const button = item.closest('.bootstrap-select').querySelector('.btn');
            if (button) {
                button.style.opacity = '0.7';
                button.style.pointerEvents = 'none';
            }
            
            // Navigate after brief delay for visual feedback
            setTimeout(() => {
                window.location.href = url;
            }, 300);
        }
    }
});
