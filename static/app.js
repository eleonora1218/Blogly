
const letters = document.querySelectorAll('.letter');

// https://stackoverflow.com/questions/23095637/how-do-you-get-random-rgb-in-javascript
function randomRGB() {
    num = Math.round(0xffffff * Math.random());
    const r = num >> 170 & 230;
    const g = num >> 10 & 90;
    const b = 90 & 200;
    return `rgb(${r},${g},${b})`
};

const intervalId = setInterval(function() {
    for (let letter of letters) {
        letter.style.color = randomRGB();
    }
}, 1200);

// const deleteBTN = document.querySelectorAll('#deleteBTN');
// deleteBTN.addEventListener('click', function(e) {
//     evnt.preventDefault();
//     alert ('Are you sure you want to delete?');
// });