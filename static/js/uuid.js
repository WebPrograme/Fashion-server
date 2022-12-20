function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

async function UserAgreed(e) {
    $(e).html(`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>`);	
    var key = 'UserAgreed',
        UserID = localStorage.getItem('UserID');
    if (!UserID) {
        UserID = uuidv4();
        localStorage.setItem('UserID', UserID);
    }
    var myElements = document.querySelectorAll('.useridInput')
    for (let i = 0; i < myElements.length; i++) {
        myElements[i].value = UserID;
    }
    
    if (document.querySelector('.alert-danger')) {
        document.querySelector('.alert-danger').style.display = 'none';
    }

    await delay(900);
    document.querySelector('.cookie').style.display = 'none';  
    localStorage.setItem('UserAgreed', true)
}

$(document).ready(function () {
    // Check if user saw the modal
    var userWelcome = localStorage.getItem('userWelcome');
        userChoice = localStorage.getItem('UserAgreed');
        UserID = localStorage.getItem('UserID');
    // Show the modal only if new user
    if (!userChoice) {
        if (!userWelcome) {
            document.querySelector('.startupModalBody').innerHTML = `<video src="https://raw.githubusercontent.com/WebPrograme/Fashion-Data/master/Fashion%20recommender%203.mp4" autoplay muted loop id="myVideo"></video>`
            $('#startupBackdrop').modal('show');
            localStorage.setItem('userWelcome', true);
        }
        document.querySelector('.cookie').style.display = 'flex';
    } else {
        var myElements = document.querySelectorAll('.useridInput')
        for (let i = 0; i < myElements.length; i++) {
            myElements[i].value = UserID;
        }
    }
});