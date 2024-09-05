const Button = [document.getElementById("Bouton1"),document.getElementById("Bouton2"),document.getElementById("Bouton3"),document.getElementById("Bouton4")];

const Validate = document.getElementById("Validate");

for (let pas = 0; pas < 4; pas++) {
  Button[pas].style.backgroundColor = 'red';
}




const InitPage = async () => {
    const response = await fetch("/add_qcm", {
      method: "GET",
    });
    const result = await response.json();
    const affirm1 = result.answer0;
    const affirm2 = result.answer1;
    const affirm3 = result.answer2;
    const affirm4 = result.answer3;

    Button[0].innerHTML = affirm1
    Button[1].innerHTML = affirm2
    Button[2].innerHTML = affirm3
    Button[3].innerHTML = affirm4
};

InitPage()


for(let i = 0; i < 4; i++){
    Button[i].addEventListener("click", () => {
        const data = new FormData();
        data.append("button", i);
            if(Button[i].style.backgroundColor == 'red'){
                Button[i].style.backgroundColor = 'green'
            }
            else{
                Button[i].style.backgroundColor = 'red'
            }
            const response = fetch("/update_qcm", {
                method: "POST",
                body: data,
  });
});
} 

