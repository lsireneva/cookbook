"use strict";
// Get the modal window
let modal = document.getElementById("date_category_modal_window");

// Get the button that opens the modal
let btn = document.getElementById("send_email_btn");

// Get the <span> element that closes the modal
let span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
    console.log('send email pressed');
    modal.style.display = "block";
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
    const send = document.querySelector("#send_email");
    send.onclick = function() {
        const email=document.querySelector("#email").value;
        modal.style.display = "none";

        const grocery_list_info = {"email": email, "grocery_list": grocery_dict};
        fetch('/send_email', {
            method: 'POST',
            body: JSON.stringify({grocery_list_info}),
            headers: {
            'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(responseJson => {
          alert(responseJson.status);
        });
    }
    
}

// when the user clicks on x, close the modal
span.onclick = function() {
    modal.style.display = "none";
  }
  
// when the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}