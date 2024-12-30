document.addEventListener("DOMContentLoaded", function() {
    document.body.style.backgroundColor = "black";
    const totalAnimationTime = 4000; // 4 seconds

    setTimeout(function() {
        document.body.style.backgroundColor = "white";
        document.querySelector('.main-loader').style.display = 'none';
    }, totalAnimationTime);

    window.scrollTo(0, 0);
});