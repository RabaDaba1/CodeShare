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