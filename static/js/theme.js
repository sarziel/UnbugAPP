
document.addEventListener('DOMContentLoaded', function() {
    // Function to set theme
    function setTheme(theme) {
        document.body.className = theme;
        localStorage.setItem('theme', theme);
        
        // Update all theme icons
        const icons = document.querySelectorAll('.theme-icon, .fa-moon, .fa-sun');
        icons.forEach(icon => {
            if (theme === 'dark-theme') {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
        });

        // Update theme-specific elements
        const elements = document.querySelectorAll('[data-theme]');
        elements.forEach(element => {
            element.setAttribute('data-theme', theme);
        });
    }
    
    // Check for saved theme preference or use default
    const savedTheme = localStorage.getItem('theme') || 'light-theme';
    setTheme(savedTheme);
    
    // Listen for theme toggle clicks
    const themeToggles = document.querySelectorAll('#theme-toggle, #header-theme-toggle, .theme-toggle');
    themeToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const currentTheme = document.body.className;
            const newTheme = currentTheme === 'light-theme' ? 'dark-theme' : 'light-theme';
            setTheme(newTheme);
        });
    });
});
