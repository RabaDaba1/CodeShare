// Get all settings icons
let settingsIcons = document.querySelectorAll('.settings-icon');

// Add event listener to each settings icon
settingsIcons.forEach(icon => {
    icon.addEventListener('click', function(event) {
        event.stopPropagation();

        // Get the dropdown menu related to this settings icon
        let dropdownMenu = this.nextElementSibling;

        // Toggle the visibility of the dropdown menu
        dropdownMenu.style.display = dropdownMenu.style.display === 'none' ? 'block' : 'none';
    });
});

// Add event listener to the document to hide dropdown menus when clicked anywhere else
document.addEventListener('click', function() {
    let dropdownMenus = document.querySelectorAll('.dropdown-menu');

    // Hide all dropdown menus
    dropdownMenus.forEach(menu => {
        menu.style.display = 'none';
    });
});

// Get all edit buttons
let editButtons = document.querySelectorAll('.edit-button');

// Add event listener to each edit button
editButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Get the post container of this edit button
        let postContainer = this.closest('.post-container');

        // Get the description, code, and output elements within this post container
        let descriptionElement = postContainer.querySelector('.description');
        let codeElement = postContainer.querySelector('.code');
        let outputElement = postContainer.querySelector('.output');

        // Replace the description, code, and output elements with textareas
        replaceWithTextarea(descriptionElement);
        replaceWithTextarea(codeElement);
        replaceWithTextarea(outputElement);

        // Hide the settings icon and show the save button
        let settingsIcon = postContainer.querySelector('.settings-icon');
        let saveButton = postContainer.querySelector('.save-button');
        settingsIcon.style.display = 'none';
        saveButton.style.display = 'block';
    });
});

// Function to replace an element with a textarea
function replaceWithTextarea(element) {
    if (element) {
        let textarea = document.createElement('textarea');
        textarea.value = element.textContent;
        textarea.style.background = 'none'; // remove background
        textarea.style.cssText = ''; // remove initial styling
        textarea.className = element.className; // copy class name from the element to the textarea
        textarea.style.width = '100%'; // add width: 100%
        textarea.style.display = 'block'; // add display: block
        textarea.style.border = 'none'; // remove border
        textarea.style.outline = 'none'; // remove outline
        textarea.onfocus = function() {
            this.style.outline = 'none';
        };

        
        element.parentNode.replaceChild(textarea, element);
    } else {
        console.error('Element does not exist');
    }
}
// Get all save buttons
let saveButtons = document.querySelectorAll('.save-button');

// Add event listener to each save button
saveButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Get the post container of this save button
        let postContainer = this.closest('.post-container');

        // Get the post ID from the post container
        let postId = postContainer.id;

        // Get the new description, code, and output
        let newDescription = postContainer.querySelector('textarea.description').value;
        let newCode = postContainer.querySelector('textarea.code').value;
        let newOutput = postContainer.querySelector('textarea.output') ? postContainer.querySelector('textarea.output').value : null;

        // Send a request to the server with the new description, code, and output
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
            return response.json();
        })
        .then(data => {
            console.log(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});