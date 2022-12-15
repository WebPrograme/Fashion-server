document.querySelector('body').addEventListener('dragover', function() {
    document.querySelector('.upload-div').style.border = '2px solid #000';
});

document.querySelector('body').addEventListener('dragleave', function() {
    document.querySelector('.upload-div').style.border = '2px dashed #2a2d3a';
});