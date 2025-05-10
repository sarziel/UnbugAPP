document.addEventListener('DOMContentLoaded', function() {
    // Get the theme toggle button
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    
    // Function to set theme
    function setTheme(theme) {
        document.body.className = theme;
        localStorage.setItem('theme', theme);
        
        // Update the icon
        if (theme === 'dark-theme') {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        } else {
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
        }
    }
    
    // Check for saved theme preference or use default
    const savedTheme = localStorage.getItem('theme') || 'light-theme';
    setTheme(savedTheme);
    
    // Listen for theme toggle click
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.body.className;
            const newTheme = currentTheme === 'light-theme' ? 'dark-theme' : 'light-theme';
            setTheme(newTheme);
        });
    }
});
