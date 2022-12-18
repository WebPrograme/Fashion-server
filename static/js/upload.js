document.querySelector('.upload-div').addEventListener('dragover', function() {
    document.querySelector('.upload-div').classList.add('upload-dragover');
});

document.querySelector('.upload-div').addEventListener('dragleave', function() {
    document.querySelector('.upload-div').classList.remove('upload-dragover');
});