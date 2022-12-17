function delay(time) {
    return new Promise(resolve => setTimeout(resolve, time));
}

async function wish(event, value) {
    event.preventDefault()
    value = value.split(' ')
    
    var source = event.target || event.srcElement;
    var store = value[0]
    var number = value[1]
    var link = value[2]
    var imgPath = value[3]
    var itemSet = [store, number, link, imgPath]
    var wishList = localStorage.getItem('wishList')
    wishList = JSON.parse(wishList)

    
    if (wishList == null || wishList.length == 0) {
        wishList = []
        wishList.push(itemSet)
        localStorage.setItem('wishList', JSON.stringify(wishList))

        if (source.nodeName && source.nodeName.toLowerCase() === 'i') {
            source.style.color = 'red'
            source.classList.add('fa-solid')        
            source.classList.toggle('wish-btn-icon-active')
            await delay(450)
            source.classList.remove('wish-btn-icon-active')
        } else {
            source.children[0].style.color = 'red'
            source.children[0].classList.add('fa-solid')
            source.children[0].classList.toggle('wish-btn-icon-active')
            await delay(450)
            source.children[0].classList.remove('wish-btn-icon-active')
        }
    } else {
        for (var j = 0; j < wishList.length; j++) {
            if (wishList[j][0] == store && wishList[j][1] == number && wishList[j][2] == link && wishList[j][3] == imgPath) {
                if (source.nodeName && source.nodeName.toLowerCase() === 'i') {
                    source.style.color = '#000'
                    source.classList.remove('fa-solid', 'wish-btn-icon-active')
                } else {
                    source.children[0].style.color = '#000'
                    source.children[0].classList.remove('fa-solid', 'wish-btn-icon-active')
                }
                wishList.splice(j, 1)
                localStorage.setItem('wishList', JSON.stringify(wishList))

                return
            }
        }
        wishList.push(itemSet)
        localStorage.setItem('wishList', JSON.stringify(wishList))

        if (source.nodeName && source.nodeName.toLowerCase() === 'i') {
            source.style.color = 'red'
            source.classList.add('fa-solid')
            source.classList.toggle('wish-btn-icon-active')
            await delay(450)
            source.classList.remove('wish-btn-icon-active')
        } else {
            source.children[0].style.color = 'red'
            source.children[0].classList.add('fa-solid')
            source.children[0].classList.toggle('wish-btn-icon-active')
            await delay(450)
            source.children[0].classList.remove('wish-btn-icon-active')
        }
    }
}

function removeWish(event, index) {
    event.preventDefault()
    var wishList = localStorage.getItem('wishList')
    wishList = JSON.parse(wishList)
    wishList.splice(index, 1)
    localStorage.setItem('wishList', JSON.stringify(wishList))
    location.reload()
}

var wishList = localStorage.getItem('wishList')
wishList = JSON.parse(wishList)
var btnPicker = document.querySelectorAll('.btn-picker')

if (wishList != null) {
    for (var i = 0; i < btnPicker.length; i++) {
        var value = btnPicker[i].value.split(' ')
        var store = value[0]
        var number = value[1]
        var link = value[2]
        var imgPath = value[3]

        for (var j = 0; j < wishList.length; j++) {
            if (wishList[j][0] == store && wishList[j][1] == number && wishList[j][2] == link && wishList[j][3] == imgPath) {
                btnPicker[i].children[0].style.color = 'red'
                btnPicker[i].children[0].classList.add('fa-solid')
            }
        }
    }
}