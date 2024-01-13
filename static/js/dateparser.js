// This script is executed when the window has finished loading
window.onload = function() {
    const dateElements = document.querySelectorAll('.date-posted');

    dateElements.forEach(element => {
        // Get the text content of the element, which is the post date
        const postDate = element.textContent;
        
        // Format the post date using the 'formatPostDate' function
        const formattedDate = formatPostDate(postDate);
        
        // Replace the text content of the element with the formatted date
        element.textContent = formattedDate;
    });
};

/**
 * Formats the post date into a human-readable string.
 * @param {string} postDate - The post date in ISO format (YYYY-MM-DDTHH:MM:SS).
 * @returns {string} The formatted post time.
 */
function formatPostDate(postDate) {
    const now = new Date();
    const diffInMilliseconds = now - new Date(postDate);
    const diffInSeconds = Math.floor(diffInMilliseconds / 1000);
    const diffInMinutes = Math.floor(diffInSeconds / 60);
    const diffInHours = Math.floor(diffInMinutes / 60);
    const diffInDays = Math.floor(diffInHours / 24);

    let postTime;

    if (diffInMinutes < 1) {
        postTime = "Posted now";
    } else if (diffInMinutes < 60) {
        postTime = `${diffInMinutes} minutes ago`;
    } else if (diffInHours < 24) {
        postTime = `${diffInHours} hours ago`;
    } else if (diffInDays < 7) {
        postTime = `${diffInDays} days ago`;
    } else {
        postTime = postDate.split('T')[0]; // postDate is in ISO format (YYYY-MM-DDTHH:MM:SS)
    }

    return postTime;
}