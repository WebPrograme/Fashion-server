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

// This function is used to show the model image
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

// This function is used to change the page
if (document.querySelector('.change_page_form')) {
    document.querySelector('.change_page_form').addEventListener('submit', function(e) {
        document.querySelector('.loader-background').style.display = 'block';
        document.querySelector('.loading-span-main').innerHTML = 'Processing...';
        $('.loader-background').show();
    });
}