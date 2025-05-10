document.addEventListener('DOMContentLoaded', () => {
    const togglePasswordVisibility = (buttonId, passwordSelector, iconId) => {
        const toggleButton = document.getElementById(buttonId);
        if (toggleButton) {
            toggleButton.addEventListener('click', () => {
                const passwordField = document.querySelector(passwordSelector);
                const icon = document.getElementById(iconId);
                const isPassword = passwordField.getAttribute('type') === 'password';

                // Cambia el tipo del campo entre "text" y "password"
                passwordField.setAttribute('type', isPassword ? 'text' : 'password');

                // Cambia el icono dinámicamente
                icon.classList.toggle('bi-eye-slash');
                icon.classList.toggle('bi-eye');
            });
        } else {
            console.warn(`No se encontró el botón con ID "${buttonId}"`);
        }
    };

    // Llama la función para cada botón de toggle
    togglePasswordVisibility('togglePassword', '[name="password"]', 'togglePasswordIcon');
    togglePasswordVisibility('togglePassword1', '[name="password1"]', 'togglePasswordIcon1');
    togglePasswordVisibility('togglePassword2', '[name="password2"]', 'togglePasswordIcon2');
});
