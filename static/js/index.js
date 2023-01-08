// Description: This script is used to show the product image or model image in the product page and some other functions
// Set all sliders status to false
var sliderStatus = [false, false, false, false, false, false, false, false, false, false]

// This function is used to reset the rest of the sliders to false
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

// This function is used to show the product image
function showProduct(index) {
    document.querySelector('.item-img-container-' + index).getElementsByClassName("model-img")[0].style.display = "none";
    document.querySelector('.item-img-container-' + index).getElementsByClassName("product-img")[0].style.display = "flex";
    document.querySelector('.item-img-container-' + index).getElementsByClassName("picker-container")[0].style.display = "flex";

    sliderStatus[index-1] = true;
    resetSliders(index-1);
}

// This function is used to show the model image
function showModel(index) {
    document.querySelector('.item-img-container-' + index).getElementsByClassName("product-img")[0].style.display = "none";
    document.querySelector('.item-img-container-' + index).getElementsByClassName("model-img")[0].style.display = "flex";
    document.querySelector('.item-img-container-' + index).getElementsByClassName("picker-container")[0].style.display = "none";

    sliderStatus[index-1] = false;
    resetSliders(index-1);
}

for (var i = 1; i <= 10; i++) {
    var element = document.getElementById('recommendBtn' + i)
    if (typeof(element) != 'undefined' && element != null) {
        document.querySelector('.item-img-container-' + i).getElementsByClassName("picker-container")[0].style.setProperty('bottom', 'calc(3.25rem + 15px)');
    }
}

// This function is used to change the page
if (document.querySelector('.change_page_form')) {
    document.querySelector('.change_page_form').addEventListener('submit', function(e) {
        document.querySelector('.loader-background').style.display = 'block';
        document.querySelector('.loading-span-main').innerHTML = 'Processing...';
        $('.loader-background').show();
    });
}

// This is used to show the top bar when the user scrolls down and the input card is not in the view
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