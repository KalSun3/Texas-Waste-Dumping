
const main = document.getElementById('main');

const images = [
    'img1.png',
    'img2.png',
    'img3.png',
    'img4.png',
    'img5.png',
    'img6.png',
    'img7.png',
    'img8.png',
    'img9.png',
    'img10.png',
    'img11.png',
    'img12.png',
    'img13.png',
    'img14.png',
    'img15.png'
]

images.forEach(img => {
    main.innerHTML += `<img src="static/images/${img}" />`
});