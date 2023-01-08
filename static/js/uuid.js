// Description: This script is used for all the functions that are used when the page is loaded
// This function is used to generate a random UUID (UserID)
function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

// This function is used to delay the execution of the code (to show the spinner in the button ;))
function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

// This function is used when the user agrees with the cookies
function UserAgreed() {
    if (localStorage.getItem('UserAgreed') == null) {
        localStorage.setItem('UserAgreed', true);
    }
}

// This is used to check if the user has already agreed with the cookies, if not, it shows the modal and the cookies
$(document).ready(function () {
    // Get the necessary variables from the local storage
    var userChoice = localStorage.getItem('UserAgreed');
        
    // If the user has not agreed with the cookies, it shows the modal and the cookies
    if (!userChoice) {
        $('#privacyBackdrop').modal('show');
    }
});