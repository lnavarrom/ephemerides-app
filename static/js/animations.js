/**
 * Utilitats per animacions suaus
 */
class Animations {
    /**
     * Fade in d'un element
     */
    static fadeIn(element, duration = 500) {
        element.style.opacity = '0';
        element.classList.remove('hidden');

        let start = null;

        function animate(timestamp) {
            if (!start) start = timestamp;
            const progress = timestamp - start;

            element.style.opacity = Math.min(progress / duration, 1);

            if (progress < duration) {
                requestAnimationFrame(animate);
            }
        }

        requestAnimationFrame(animate);
    }

    /**
     * Fade out d'un element
     */
    static fadeOut(element, duration = 500) {
        let start = null;

        function animate(timestamp) {
            if (!start) start = timestamp;
            const progress = timestamp - start;

            element.style.opacity = Math.max(1 - progress / duration, 0);

            if (progress < duration) {
                requestAnimationFrame(animate);
            } else {
                element.classList.add('hidden');
            }
        }

        requestAnimationFrame(animate);
    }

    /**
     * Shake animation per errors
     */
    static shake(element) {
        element.classList.add('shake');

        setTimeout(() => {
            element.classList.remove('shake');
        }, 500);
    }
}

// Afegir classe CSS per shake
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    .shake {
        animation: shake 0.5s ease;
    }
`;
document.head.appendChild(style);
