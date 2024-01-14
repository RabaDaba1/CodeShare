const settingsIcons = document.querySelectorAll('.settings-icon');
const editButtons = document.querySelectorAll('.edit-button');
const saveButtons = document.querySelectorAll('.save-button');
const shareButtons = document.querySelectorAll('.share-button');

// Add event listeners
settingsIcons.forEach(icon => icon.addEventListener('click', toggleDropdownMenu));
editButtons.forEach(button => button.addEventListener('click', editPost));
document.addEventListener('click', hideAllDropdownMenus);
saveButtons.forEach(button => {
    button.addEventListener('click', handleSaveButtonClick);
});
shareButtons.forEach(button => {
    button.addEventListener('click', handleShareButtonClick);
});

// Function to toggle dropdown menu
function toggleDropdownMenu(event) {
    event.stopPropagation();
    const dropdownMenu = this.nextElementSibling;
    dropdownMenu.classList.toggle('hidden');
}

// Function to hide all dropdown menus
function hideAllDropdownMenus() {
    const dropdownMenus = document.querySelectorAll('.dropdown-menu');
    dropdownMenus.forEach(menu => menu.classList.add('hidden'));
}

// Function to edit post
function editPost() {
    const postContainer = this.closest('.post-container');
    const descriptionElement = postContainer.querySelector('.description');
    const codeElement = postContainer.querySelector('.code');
    const outputElement = postContainer.querySelector('.output');
    replaceWithTextarea(descriptionElement);
    replaceWithTextarea(codeElement);
    replaceWithTextarea(outputElement);
    const settingsIcon = postContainer.querySelector('.settings-icon');
    const saveButton = postContainer.querySelector('.save-button');
    settingsIcon.classList.add('hidden');
    saveButton.classList.remove('hidden');
}

// Function to replace an element with a textarea
function replaceWithTextarea(element) {
    if (element) {
        let textarea = document.createElement('textarea');
        textarea.value = element.textContent;
        textarea.className = element.className;
        
        textarea.style.cssText = ''; // remove initial styling
        textarea.style.width = '100%'; // add width: 100%
        textarea.style.display = 'block'; // add display: block
        textarea.style.border = 'none'; // remove border
        textarea.style.outline = 'none'; // remove outline
        
        textarea.onfocus = function() {
            this.style.outline = 'none';
        };

        element.parentNode.replaceChild(textarea, element);
    }
}

// Function to replace textarea with original element
function replaceTextareaWithOriginal(textarea, newValue, originalTag) {
    if (textarea) {
        const element = document.createElement(originalTag);
        element.textContent = newValue;
        textarea.parentNode.replaceChild(element, textarea);
    } else {
        console.error('Textarea does not exist');
    }
}

// Function to handle save button click
function handleSaveButtonClick() {
    const postContainer = this.closest('.post-container');
    const postId = postContainer.id;

    const newDescription = postContainer.querySelector('textarea.description').value;
    const newCode = postContainer.querySelector('textarea.code').value;
    const newOutput = postContainer.querySelector('textarea.output') ? postContainer.querySelector('textarea.output').value : null;

    fetch(`/post/${postId}/edit`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            description: newDescription,
            code: newCode,
            output: newOutput,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    })
    .then(() => {
        const descriptionElement = postContainer.querySelector('textarea.post-description');
        const codeElement = postContainer.querySelector('textarea.post-code');
        const outputElement = postContainer.querySelector('textarea.post-output');

        replaceTextareaWithOriginal(descriptionElement, newDescription, 'p');
        replaceTextareaWithOriginal(codeElement, newCode, 'pre');
        replaceTextareaWithOriginal(outputElement, newOutput, 'pre');
    })
    .catch(error => console.error('Error:', error));
}

// Function to handle share button click
function handleShareButtonClick(event) {
    const postLink = this.getAttribute('data-post-link');

    // Create a temporary input to hold the post link
    const tempInput = document.createElement('input');
    tempInput.style.position = 'absolute';
    tempInput.style.left = '-1000px';
    tempInput.style.top = '-1000px';
    tempInput.value = postLink;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);

    // Show tooltip
    const tooltip = document.getElementById('tooltip');
    tooltip.style.left = `${event.pageX}px`; // Position the tooltip at the mouse position
    tooltip.style.top = `${event.pageY - 30}px`; // Position the tooltip 30px above the mouse position
    tooltip.style.display = 'block'; // Show the tooltip

    // Hide tooltip after 500 milliseconds
    setTimeout(() => {
        tooltip.style.display = 'none';
    }, 500);
}