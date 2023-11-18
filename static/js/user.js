// Get the elements
const elements = {
    modal: document.getElementById('modal'),
    followersSection: document.getElementById('followersSection'),
    followingSection: document.getElementById('followingSection'),
    followersTab: document.getElementById('followersTab'),
    followingTab: document.getElementById('followingTab'),
    followersNumber: document.getElementById('followersLink'),
    followingNumber: document.getElementById('followingLink'),
    close: document.getElementById('close')
};

// Function to open modal and show followers
function showFollowers() {
    elements.modal.style.display = 'block';
    elements.followersSection.style.display = 'block';
    elements.followingSection.style.display = 'none';
    switchTab(elements.followersTab, elements.followingTab);
}

// Function to open modal and show following
function showFollowing() {
    elements.modal.style.display = 'block';
    elements.followersSection.style.display = 'none';
    elements.followingSection.style.display = 'block';
    switchTab(elements.followingTab, elements.followersTab);
}

// Function to switch active tab
function switchTab(activeTab, inactiveTab) {
    activeTab.classList.add('text-indigo-600');
    activeTab.classList.remove('text-neutral-500');
    inactiveTab.classList.add('text-neutral-500');
    inactiveTab.classList.remove('text-indigo-600');
}

// Function to close modal
function closeModal() {
    elements.modal.style.display = 'none';
}

// Add event listeners to numbers
elements.followersNumber.addEventListener('click', showFollowers);
elements.followingNumber.addEventListener('click', showFollowing);

// Add event listeners to tabs
elements.followersTab.addEventListener('click', showFollowers);
elements.followingTab.addEventListener('click', showFollowing);

// Add event listener to close button
elements.close.addEventListener('click', closeModal);