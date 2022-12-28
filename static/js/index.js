function updateGender(){
    console.log('Gender updated')
    $('.loader-background').show();
    document.getElementById('gender-form').submit()
}

var sliderStatus = [false, false, false, false, false, false, false, false, false, false]

function resetSliders(index) {
    for (var i = 0; i < sliderStatus.length; i++) {
        if (i != index && sliderStatus[i] == true) {
            sliderStatus[i] = false
            if (i == 0) {
                document.getElementById('owl-carousel-basic').getElementsByClassName("picker-container")[0].style.display = "none";
                $('#owl-carousel-basic').trigger('next.owl.carousel');
            } else {
                document.getElementById('owl-carousel-basic-' + (Number(i) + 1)).getElementsByClassName("picker-container")[0].style.display = "none";
                $('#owl-carousel-basic-' + (Number(i) + 1)).trigger('next.owl.carousel');
            }
        }
    }
}

function showProduct(index) {
    if (index == 1) {
        $('#owl-carousel-basic').trigger('prev.owl.carousel');
        document.getElementById('owl-carousel-basic').getElementsByClassName("picker-container")[0].style.display = "flex";
    } else {
        $('#owl-carousel-basic-' + index).trigger('prev.owl.carousel');
        document.getElementById('owl-carousel-basic-' + index).getElementsByClassName("picker-container")[0].style.display = "flex";
    }
    sliderStatus[index-1] = true;
    resetSliders(index-1);
}

function showModel(index) {
    if (index == 1) {
        $('#owl-carousel-basic').trigger('next.owl.carousel');
        document.getElementById('owl-carousel-basic').getElementsByClassName("picker-container")[0].style.display = "none";
    } else {
        $('#owl-carousel-basic-' + index).trigger('next.owl.carousel');
        document.getElementById('owl-carousel-basic-' + index).getElementsByClassName("picker-container")[0].style.display = "none";
    }
    sliderStatus[index-1] = false;
    resetSliders(index-1);
}

if (document.querySelector('.change_page_form')) {
    document.querySelector('.change_page_form').addEventListener('submit', function(e) {
        document.querySelector('.loader-background').style.display = 'block';
        document.querySelector('.loading-span-main').innerHTML = 'Processing...';
        $('.loader-background').show();
    });
}

var shareMethod = document.getElementById('share-method').value;
var shareStore = document.getElementById('share-store').value;
shareMethod = shareMethod.toUpperCase()

if (shareMethod != '') {
    if (shareStore != 'Link of an image' && shareStore != 'Ready2Go') {
        var barHeader = document.querySelector('.top-bar h4');
        barHeader.innerHTML = shareMethod + ' | ' + shareStore;
    } else {
        var barHeader = document.querySelector('.top-bar h4');
        barHeader.innerHTML = shareMethod;
    }
} else {
    var barHeader = document.querySelector('.top-bar h4');
    barHeader.innerHTML = 'IMAGE';
}

function Utils() {

}

Utils.prototype = {
    constructor: Utils,
    isElementInView: function (element, fullyInView) {
        var pageTop = $(window).scrollTop();
        var pageBottom = pageTop + $(window).height();
        var elementTop = $(element).offset().top;
        var elementBottom = elementTop + $(element).height();

        if (fullyInView === true) {
            return ((pageTop < elementTop) && (pageBottom > elementBottom));
        } else {
            return ((elementTop <= pageBottom) && (elementBottom >= pageTop));
        }
    }
};

var Utils = new Utils();
var topBar = document.querySelector('.top-bar-container');

document.addEventListener('scroll', function() {
    var isElementInView = Utils.isElementInView($('.input-card'), false);

    if (isElementInView) {
        if (topBar.classList.contains('top-bar-visible')) {
            topBar.classList.remove('top-bar-visible');
        }
    } else {
        topBar.classList.add('top-bar-visible');
    }
});