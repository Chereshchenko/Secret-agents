const themeToggle = document.getElementById('theme-toggle');
        const body = document.getElementById('body');

        themeToggle.addEventListener('click', () => {
            body.classList.toggle('bg-dark');
            body.classList.toggle('text-light');

            if (body.classList.contains('bg-dark')) {
                themeToggle.innerHTML = '<i class="fas fa-sun"></i> Светлая тема';
            } else {
                themeToggle.innerHTML = '<i class="fas fa-moon"></i> Темная тема';
            }
        });