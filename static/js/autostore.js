var input = document.getElementById('articleLink');

function get_store(link) {
    if (link.includes('hm.com')) {
        store = 'H&M'
    } else if (link.includes('zara.com')) {
        store = 'Zara'
    } else if (link.includes('bershka.com')) {
        store = 'Bershka'
    } else if (link.includes('pullandbear.com')) {
        store = 'Pull&Bear'
    } else if (link.includes('stradivarius.com')) {
        store = 'Stradivarius'
    } else if (link.includes('weekday.com')) {
        store = 'Weekday'
    } else if (link.includes('hollisterco.com')) {
        store = 'Hollister (+ Social Tourist)'
    } else if (link.includes('Guess.com')) {
        store = 'Guess'
    } else if (link.includes('reserved.com')) {
        store = 'Reserved'
    } else if (link.includes('mango.com')) {
        store = 'Mango'
    } else if (link.includes('c-and-a.com.com')) {
        store = 'C&A'
    } else if (link.includes('newyorker.de')) {
        store = 'New Yorker'
    } else if (link.includes('/aerie/')) {
        store = 'Aerie'
    } else if (link.includes('ae.com')) {
        store = 'American Eagle'
    } else if (link.includes('vrggrl.com')) {
        store = 'VRG GRL'
    } else if (link.includes('abercrombie.com')) {
        store = 'Abercrombie & Fitch'
    } else if (link.includes('express.com')) {
        store = 'Express'
    } else if (link.includes('everlane.com')) {
        store = 'Everlane'
    } else if (link.includes('aboutyou')) {
        store = 'About You'
    } else {
        store = 'Unknown'
    }
    return store
}

input.addEventListener('keyup', function() {
    var link = input.value;
    store = get_store(link);
    
    if (store != 'Unknown') {
        var link_confirm_btn = document.getElementById('link-confirm-btn');
        document.getElementById('link-store-select').value = store;
        link_confirm_btn.disabled = false
        link_confirm_btn.focus()
        link_confirm_btn.style.boxShadow = '0 0 0 0.3rem rgb(38 161 235 / 50%)';
        link_confirm_btn.style.transition = "all .3s";
    }
});