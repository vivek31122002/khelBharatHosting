document.addEventListener("DOMContentLoaded", function() {
    const contents = document.querySelectorAll('.scroller2');

    function checkVisibility() {
        const triggerBottom = window.innerHeight * 0.8;
        const triggerTop = window.innerHeight * 0.2;

        contents.forEach(scroller2 => {
            const contentTop = scroller2.getBoundingClientRect().top;
            const contentBottom = scroller2.getBoundingClientRect().bottom;

            if (contentTop < triggerBottom && contentBottom > triggerTop) {
                scroller2.classList.add('visible');
            } else {
                scroller2.classList.remove('visible');
            }
        });
    }

    window.addEventListener('scroll', checkVisibility);
    checkVisibility();
});
