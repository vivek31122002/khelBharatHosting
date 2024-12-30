document.addEventListener('DOMContentLoaded', () => {
    let valueDisplays = document.querySelectorAll(".num");
    let interval = 4000;
  
    let observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          let valueDisplay = entry.target;
          let startValue = 0;
          let endValue = parseInt(valueDisplay.getAttribute("data-val"));
          let duration = Math.floor(interval / endValue);
          
          let counter = setInterval(function () {
            startValue += 1;
            valueDisplay.textContent = startValue;
            if (startValue == endValue) {
              clearInterval(counter);
            }
          }, duration);
          
          observer.unobserve(valueDisplay); // Stop observing while counting to avoid multiple triggers
        } else {
          observer.observe(entry.target); // Re-observe the element when it exits the viewport
        }
      });
    }, { threshold: 0.1 }); // Adjust threshold as needed
  
    valueDisplays.forEach(valueDisplay => {
      observer.observe(valueDisplay);
    });
  });