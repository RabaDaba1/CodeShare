// Post creation section
document.getElementById('create-post-button').addEventListener('click', function() {
    document.getElementById('create-post-section').style.display = '';
});
  
document.getElementById('output').style.display = 'none';

document.getElementById('output-checkbox').addEventListener('change', function() {
const outputSection = document.getElementById('output');
if (this.checked) {
    outputSection.disabled = false;
    outputSection.style.display = '';
} else {
    outputSection.disabled = true;
    outputSection.style.display = 'none';
}
});

// Like button
document.querySelectorAll('.like').forEach(button => {
    button.addEventListener('click', function() {
      // Toggle the button appearance
      const heartIcon = this.firstChild;
      heartIcon.classList.toggle('far');
      heartIcon.classList.toggle('fas');
    });
  });

  // Post creation section
document.getElementById('create-post-button').addEventListener('click', function() {
    document.getElementById('create-post-section').style.display = '';
});
  
document.getElementById('output').style.display = 'none';

document.getElementById('output-checkbox').addEventListener('change', function() {
    const outputSection = document.getElementById('output');
    if (this.checked) {
        outputSection.disabled = false;
        outputSection.style.display = '';
    } else {
        outputSection.disabled = true;
        outputSection.style.display = 'none';
    }
});

// Update like button appearance after form submission
document.querySelectorAll('.like').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        // Toggle the button appearance
        const heartIcon = this.firstChild;
        heartIcon.classList.toggle('far');
        heartIcon.classList.toggle('fas');
    });
});