function Redirection1() {
    window.location = "http://127.0.0.1:5000/hello"
};


const classic_button = document.getElementById("Bouton1");
const qcm_button = document.getElementById("Bouton2");

classic_button.addEventListener('click', function () {
    window.location.href = "/hello"
});





classic_button.style.backgroundColor = 'green';
qcm_button.style.backgroundColor = 'red';
