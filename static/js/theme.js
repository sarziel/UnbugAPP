document.addEventListener('DOMContentLoaded', function() {
    // Get the theme toggle button
    const themeToggle = document.getElementById('header-theme-toggle');
    
    // Function to set theme
    function setTheme(theme) {
        document.body.className = theme;
        localStorage.setItem('theme', theme);
        
        // Update all theme icons
        const icons = document.querySelectorAll('#header-theme-toggle i');
        icons.forEach(icon => {
            if (theme === 'dark-theme') {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            }
        });
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
