// Smooth scrolling effect with offset
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href').substring(1);  // Get the target section ID
        const targetSection = document.getElementById(targetId);
        
        // Scroll to the target position with an offset (e.g., -50px)
        window.scrollTo({
            top: targetSection.offsetTop - 50,  // Adjust this value as needed for your offset
            behavior: 'smooth'
        });
    });
});


// Highlight active link
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-link');
    let current = "";

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        if (scrollY >= sectionTop) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// Update the progress bar based on scroll position
window.addEventListener("scroll", function() {
    const progressBar = document.getElementById("progress-bar");
    const totalHeight = document.body.scrollHeight - window.innerHeight;
    const progress = (window.scrollY / totalHeight) * 100;
    progressBar.style.width = progress + "%";
});
