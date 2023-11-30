function loadSearchData(data) {
    let ingredients = data;
    let list = document.getElementById('list');
    ingredients.forEach((ingredient) => {
        let a = document.createElement("a");
        a.innerText = country;
        a.classList.add("listItem"); 
        list.appendChild(a);
    })
}

function myFunc(data) {
    return data
}