// Description: This script is used to submit the form when the user clicks on a ready2go card and to show the modal effects when the user scrolls the modal body
// This is used to submit the form when the user clicks on a ready2go card
document.querySelectorAll('.ready2go-card').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        loading('processing');
        document.getElementById('forselected-input').value = anchor.getAttribute('data-title')
        document.getElementById('forselected-form').submit()
    });
});

// This is used to show the modal effects when the user scrolls the modal body
document.querySelectorAll('.modal-dialog-scrollable .modal-body').forEach(anchor => {
    anchor.addEventListener('scroll', function(e){
        var modal_body = $('.modal-dialog-scrollable .modal-body')[9];
        var modal_scrollTop = modal_body.scrollTop;
        var modal_scrollHeight = modal_body.scrollHeight;        
        var modal_innerHeight = modal_body.offsetHeight;        
        
        if (modal_scrollTop + modal_innerHeight >= modal_scrollHeight) {
            document.querySelector('.scroll-shadow-bottom').style.display = 'none';
        } else if (modal_scrollTop + modal_innerHeight < modal_scrollHeight) {
            document.querySelector('.scroll-shadow-bottom').style.display = 'block';
        }
        
        if (modal_scrollTop == 0) {
            document.querySelector('.scroll-shadow-top').style.display = 'none';
        } else if (modal_scrollTop > 0) {
            document.querySelector('.scroll-shadow-top').style.display = 'block';
        }
    })
})