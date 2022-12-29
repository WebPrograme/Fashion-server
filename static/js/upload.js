// Description: This script is used to change the upload div style when the user drags a file over the upload button
// This is used to change the upload div style when the user drags a file over the upload button
document.querySelector('.upload-div').addEventListener('dragover', function() {
    document.querySelector('.upload-div').classList.add('upload-dragover');
});

// This is used to change the upload div style when the user drags a file out of the upload button
document.querySelector('.upload-div').addEventListener('dragleave', function() {
    document.querySelector('.upload-div').classList.remove('upload-dragover');
});