var shareID = document.getElementById('share-id').value;
var shareStore = document.getElementById('share-store').value;
var shareContent = document.getElementById('share-content').value;
var shareMethod = document.getElementById('share-method').value;

if (shareMethod == 'link') {
    var shareURL = 'https://fashion-recommender.onrender.com/predict/?UserID=' + shareID + '&store=' + shareStore + '&link=' + shareContent; 
} else if (shareMethod == 'number') {
    var shareURL = 'https://fashion-recommender.onrender.com/predict/?UserID=' + shareID + '&store=' + shareStore + '&number=' + shareContent; 
} else {
    var shareURL = 'https://fashion-recommender.onrender.com/predict/?UserID=' + shareID + '&forselected-input=' + shareStore + ' ' + shareContent; 
}

const shareData = {
    title: 'Fashion recommender',
    text: 'Open this link to see the results of the shared image!',
    url: shareURL
};

document.querySelector('.share-btn').addEventListener('click', function(){
    try {
        navigator.share(shareData);
    } catch (err) {
        console.log(`Error: ${err}`)
    }
});