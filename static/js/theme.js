document.addEventListener('DOMContentLoaded', function() {
    function setTheme(theme) {
        document.body.classList.remove('light-theme', 'dark-theme');
        document.body.classList.add(theme);
        localStorage.setItem('theme', theme);

        const icons = document.querySelectorAll('.theme-icon, .fa-moon, .fa-sun');
        icons.forEach(icon => {
            icon.classList.remove('fa-moon', 'fa-sun');
            icon.classList.add(theme === 'dark-theme' ? 'fa-sun' : 'fa-moon');
        });
    }

    const savedTheme = localStorage.getItem('theme') || 'light-theme';
    setTheme(savedTheme);

    document.querySelectorAll('#theme-toggle, #header-theme-toggle, .theme-toggle').forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            const currentTheme = document.body.classList.contains('dark-theme') ? 'dark-theme' : 'light-theme';
            const newTheme = currentTheme === 'light-theme' ? 'dark-theme' : 'light-theme';
            setTheme(newTheme);
        });
    });
});