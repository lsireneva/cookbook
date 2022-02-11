"use strict";
// Get the modal window
let modal = document.getElementById("glModal");

// Get the button that opens the modal
let btn = document.getElementById("send_email_btn");

// Get the element that closes the modal
let closebtn = document.getElementById("model-close");

//When the user clicks the button, open the modal 
btn.onclick = function() {
     console.log('send email pressed');
     modal.style.display = "block";    
}

function sendEmail(element, start_day, end_day) {
    console.log("send in modal pressed");
    //modal.style.display = "block";
    let grocery_dict ={};

    const grocery_list = document.querySelectorAll("#grocery_list"); 
    
    for (let i = 0; i < grocery_list.length; i++) {
        let block=grocery_list[i];
        let aisle_name=block.children[0].innerText;
        grocery_dict[aisle_name]=[];
        for (let j = 1; j < block.children.length; j++){ 
            console.log(block.children[j].innerText);
            grocery_dict[aisle_name].push(block.children[j].innerText);
        }
    }
    console.log("dictionary");
    console.log(grocery_dict);

    const email=document.querySelector("#email").value;
    modal.style.display = "none";

    const grocery_list_info = {"email": email, "start_day": start_day, "end_day": end_day, "grocery_list": grocery_dict};
    fetch('/send_email', {
        method: 'POST',
        body: JSON.stringify({grocery_list_info}),
        headers: {
        'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {
        let myAlert = document.getElementById('glToast');
        let toastMessage = document.getElementById('toast_message');
        toastMessage.innerText=responseJson.status;
        let myToast = bootstrap.Toast.getOrCreateInstance(myAlert);
        myToast.show();      
    });
    
}

// when the user clicks on x, close the modal
closebtn.onclick = function() {
    modal.style.display = "none";
  }
  
// when the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}