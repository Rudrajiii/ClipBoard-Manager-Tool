// Clipy Website Interactive Features

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeTerminal();
    addSmoothScrolling();
    addCommandAnimation();
});

/**
 * Initialize terminal-like interactions
 */
function initializeTerminal() {
    // Add console log for terminal startup
    console.log('%c███ CLIPY TERMINAL INITIALIZED ███', 'color: #e7f98b; font-weight: bold;');
    
    // Animate sections on scroll
    observeSections();
    
    // Add keyboard shortcuts
    addKeyboardShortcuts();
}

/**
 * Observe sections for scroll animations
 */
function observeSections() {
    const sections = document.querySelectorAll('.output-section');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                animateSection(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    sections.forEach(section => {
        observer.observe(section);
    });
}

/**
 * Animate section when it becomes visible
 */
function animateSection(section) {
    section.style.opacity = '0';
    section.style.transform = 'translateX(-20px)';
    
    setTimeout(() => {
        section.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        section.style.opacity = '1';
        section.style.transform = 'translateX(0)';
    }, 100);
}

/**
 * Add smooth scrolling for better UX
 */
function addSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId) {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

/**
 * Add terminal-like command animations
 */
function addCommandAnimation() {
    const commands = document.querySelectorAll('.command:not(.typing-text)');
    
    commands.forEach((cmd, index) => {
        cmd.style.opacity = '0';
        
        setTimeout(() => {
            cmd.style.transition = 'opacity 0.3s ease';
            cmd.style.opacity = '1';
        }, 200 * index);
    });
}

/**
 * Add keyboard shortcuts for terminal feel
 */
function addKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K to scroll to top (like clearing terminal)
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
            console.log('%c$ clear', 'color: #99a659;');
        }
        
        // Ctrl/Cmd + D to scroll to download section
        if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
            e.preventDefault();
            const downloadSection = document.querySelector('.btn-primary');
            if (downloadSection) {
                downloadSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            console.log('%c$ cd download/', 'color: #99a659;');
        }
    });
}

/**
 * Add particle effect on button hover (optional enhancement)
 */
function addButtonEffects() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        button.addEventListener('click', function() {
            // Create ripple effect
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.5)';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.pointerEvents = 'none';
            ripple.style.animation = 'ripple 0.6s ease-out';
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

// Initialize button effects
addButtonEffects();

/**
 * Console Easter Egg
 */
console.log('%c', 'font-size: 1px; padding: 100px 150px; background: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDAiIGhlaWdodD0iMjAwIj48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1mYW1pbHk9Im1vbm9zcGFjZSIgZm9udC1zaXplPSIyNCIgZmlsbD0iI2U3Zjk4YiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZG9taW5hbnQtYmFzZWxpbmU9Im1pZGRsZSI+Q0xJUFk8L3RleHQ+PC9zdmc+) no-repeat;');
console.log('%cWelcome to Clipy!', 'color: #e7f98b; font-size: 18px; font-weight: bold;');
console.log('%cKeyboard Shortcuts:', 'color: #99a659; font-size: 14px; font-weight: bold;');
console.log('%c  Ctrl/Cmd + K : Scroll to top', 'color: #a9bca9;');
console.log('%c  Ctrl/Cmd + D : Jump to download', 'color: #a9bca9;');
console.log('%c\nCreated by Rudra 💚', 'color: #ddf8dd; font-style: italic;');

// Add CSS animation for ripple effect
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Expose Clipy object to window for debugging
window.clipy = {
    version: '1.0.0',
    author: 'Rudra'
};
