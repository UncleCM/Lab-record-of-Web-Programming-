document.getElementById('changeColor').addEventListener('click', changeColor);

function changeColor() {
    const paragraphs = document.querySelectorAll('p');
    paragraphs.forEach(paragraph => {
        paragraph.style.color = "blue";
    });
}
