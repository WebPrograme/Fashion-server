// Description: This file contains the code for the "Share" feature.
// Get the necessary values from the form
var shareID = document.getElementById('share-id').value;
var shareStore = document.getElementById('share-store').value;
var shareContent = document.getElementById('share-content').value;
var shareMethod = document.getElementById('share-method').value;

// Create the URL to share
// If the user chose to share a input link, the URL will be like this:
if (shareMethod == 'link') {
    var shareURL = 'https://fashion-recommender.onrender.com/predict/?UserID=' + shareID + '&store=' + shareStore + '&link=' + shareContent; 
} else if (shareMethod == 'number') { // If the user chose to share a input number, the URL will be like this:
    var shareURL = 'https://fashion-recommender.onrender.com/predict/?UserID=' + shareID + '&store=' + shareStore + '&number=' + shareContent; 
} else { // If the user chose to share a Ready2Go image, the URL will be like this:
    var shareURL = 'https://fashion-recommender.onrender.com/predict/?UserID=' + shareID + '&forselected-input=' + shareStore + ' ' + shareContent; 
}

// Create the data to share
const shareData = {
    title: 'Fashion recommender',
    text: 'Open this link to see the results of the shared image!',
    url: shareURL
};

// Add the event listener to the share button
document.querySelector('.share-btn').addEventListener('click', function(){
    try {
        // Share the data
        navigator.share(shareData);
    } catch (err) {
        // If the user's browser doesn't support the share API, show an error message
        console.log(`Error: ${err}`)
    }
});