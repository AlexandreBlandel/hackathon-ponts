const Button1 = document.getElementById("Bouton1");
const Button2 = document.getElementById("Bouton2");
const Button3 = document.getElementById("Bouton3");
const Button4 = document.getElementById("Bouton4");
const Validate = document.getElementById("Validate");



const InitPage = async () => {
    const response = await fetch("/add_qcm", {
      method: "GET",
    });
    const result = await response.json();
    const affirm1 = result.answer0;
    const affirm2 = result.answer1;
    const affirm3 = result.answer2;
    const affirm4 = result.answer3;

    Button1.innerHTML = affirm1
    Button2.innerHTML = affirm2
    Button3.innerHTML = affirm3
    Button4.innerHTML = affirm4
};

InitPage()

