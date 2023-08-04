function clearAll() {
    let selectElem = document.querySelector('#business');
    let inputElem = document.querySelector('#item-name');
    let numElem = document.querySelector('#item-num');
    let divElem = document.querySelector('#item-fetched');
    let warnElem = document.querySelector('#warn');
    selectElem.value = "";
    inputElem.value = "";
    numElem.innerHTML = "";
    divElem.innerHTML = "";
    warnElem.innerHTML = "";
    warnElem.style.display = 'none';
};

function submit(elem) {
    let loaderElem = document.querySelector('#loader');
    let selectElem = document.querySelector('#business');
    let inputElem = document.querySelector('#item-name');
    let warnElem = document.querySelector('#warn');
    let iconElem = document.querySelectorAll('img.icon');

    let [business, item] = [selectElem.value, inputElem.value.trim()];

    if (business == "" && item == "") {
        warnElem.textContent = 'Please select a grocery store and enter a valid item.';
        warnElem.style.display = 'block';
    } else if (business != "" && item == "") {
        warnElem.textContent = 'Please enter a valid item.';
        warnElem.style.display = 'block';
    } else if (business == "" && item != "") {
        warnElem.textContent = 'Please select a grocery store.';
        warnElem.style.display = 'block';
    } else {
        warnElem.textContent = '';
        warnElem.style.display = 'none';
        loaderElem.style.display = 'block';

        // disable input text and selector
        selectElem.disabled = true;
        inputElem.disabled = true;
        elem.disabled = true;
        for (let i = 0; i < iconElem.length; i++) {
            iconElem[i].style.pointerEvents = 'none';
        }

        fetch('/get-item/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'business': business, 'item': item })
        }).then(function (response) {
            return response.json();
        }).then(function (data) {
            let numElem = document.querySelector('#item-num');
            let divElem = document.querySelector('#item-fetched');
            let numItem = data.length;
            divElem.innerHTML = "";
            loaderElem.style.display = 'none';

            // undisable input text and selector
            selectElem.disabled = false;
            inputElem.disabled = false;
            elem.disabled = false;
            for (let i = 0; i < iconElem.length; i++) {
                iconElem[i].style.pointerEvents = 'auto';
            }

            if (numItem > 0) {
                numElem.innerHTML = numItem + " items found in " + business;

                for (let i = 0; i < numItem; i++) {
                    let item = data[i];
                    divElem.innerHTML += '<div onclick="jumpToComparison(this);"' +
                        'onmouseover="over(this);"' +
                        'onmouseout="out(this);"' +
                        'class="item"><div class="prop-item">' +
                        '<img width="130px" height="130px" src="' +
                        item.img + '"/></div><div class="prop-item" style="font-weight: bold;">' +
                        item.name + '</div><div class="prop-item">' +
                        item.volume + '</div><div class="prop-item">' +
                        item.price + '</div><div class="prop-item">' +
                        item.unit_price + '</div></div>'
                };
            } else {
                numElem.innerHTML = "Item not found. Please try again";
            }

        })
    };
};

function over(elem) {
    elem.style.backgroundColor = '#B5EAAA';
}

function out(elem) {
    elem.style.backgroundColor = '#C3FDB8';
}

function goBack() {
    window.history.back();
}

function jumpToComparison(elem) {
    let loaderElem = document.querySelector('#loader');
    let selectElem = document.querySelector('#business');
    let inputElem = document.querySelector('#item-name');
    let submitElem = document.querySelector('#submit-btn');
    let itemElems = document.querySelectorAll('div.item');  // get all item elements
    let iconElem = document.querySelectorAll('img.icon');  // get all icons

    let business = selectElem.value;
    let item = elem.childNodes[1].innerText;
    let item_cleaned = item.replace(business, "").trim();

    // disable selector, input box, submit button, and all items to be editable
    loaderElem.style.display = 'block';
    selectElem.disabled = true;
    inputElem.disabled = true;
    submitElem.disabled = true;
    for (let i = 0; i < itemElems.length; i++) {
        itemElems[i].style.pointerEvents = 'none';
    }
    for (let i = 0; i < iconElem.length; i++) {
        iconElem[i].style.pointerEvents = 'none';
    }

    fetch('/get-item/fetch-compare/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'item': item_cleaned })
    })
        .then(response => response.json())  // array function
        .then(data => {
            // jump to another html page
            window.location.href = '/get-item/display-compare/?data=' + encodeURIComponent(JSON.stringify(data));
        })
        .catch(error => console.error('Error', error));
};

