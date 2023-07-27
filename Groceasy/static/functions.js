function clearAll() {
    let selectElem = document.querySelector('#business');
    let inputElem = document.querySelector('#item-name');
    let numElem = document.querySelector('#item-num');
    let divElement = document.querySelector('#item-fetched');
    selectElem.value = "";
    inputElem.value = "";
    numElem.innerHTML = "";
    divElement.innerHTML = "";
};

function submit() {
    let selectElem = document.querySelector('#business');
    let inputElem = document.querySelector('#item-name');
    let warnElem = document.querySelector('#warn');

    let [business, item] = [selectElem.value, inputElem.value];

    if (business == "" && item == "") {
        warnElem.textContent = 'Please select a grocery store and enter an item.';
        warnElem.style.display = 'block';
    } else if (business != "" && item == "") {
        warnElem.textContent = 'Please enter an item.';
        warnElem.style.display = 'block';
    } else if (business == "" && item != "") {
        warnElem.textContent = 'Please select a grocery store.';
        warnElem.style.display = 'block';
    } else {
        warnElem.style.display = 'none';

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

            if (numItem > 0) {
                numElem.innerHTML = numItem + " items found";

                for (let i = 0; i < numItem; i++) {
                    let item = data[i];
                    divElem.innerHTML += '<div class="item"><div class="prop-item">' +
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