"use strict";
// Get the modal window
let modal = document.getElementById("date_category_modal_window");

// Get the button that opens the modal
let btn = document.getElementById("add_meal_plan");

// Get the <span> element that closes the modal
let span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
    console.log('add_meal_plan pressed');
    modal.style.display = "block";
    // Get the button in the modal window
    const add = document.querySelector("#add_date_category");
    add.onclick = function() {
        const meal_date = document.querySelector("#meal_date").value;
        //console.log(document.querySelector("#meal_date"));
        console.log(meal_date);
    
        const meal_category = document.querySelector("#meal_category").value;
        //console.log(document.querySelector("#meal_category"));
        console.log(meal_category);
    
        modal.style.display = "none";

        const recipe_id = document.querySelector("#recipe_id").innerHTML;
        console.log(recipe_id);
        const title = document.querySelector("#recipe_title").innerHTML;
        console.log(title);
        
        const image=document.querySelector("#recipe_image").getAttribute("src");
        //console.log(image);
        const time = document.querySelector("#time").innerHTML;
        //console.log(time);
        const servings = document.querySelector("#servings").innerHTML;
        //console.log(servings);
        const calories = document.querySelector("#calories").innerHTML;
        //console.log(calories);
        const fat = document.querySelector("#fat").innerHTML;
        //console.log(fat);
        const protein = document.querySelector("#protein").innerHTML;
        //console.log(protein);
        const carbs = document.querySelector("#carbs").innerHTML;
        //console.log(carbs);
    
        let elem = document.querySelector("#dish_type");
        let dish_type = elem ? elem.innerHTML : "";
        
        if(!dish_type) {
          dish_type="general"
        }
        
        const ingredients = []
        const item=document.querySelectorAll("#item");
        for (let i = 0; i < item.length; i++) {
          
          let block=item[i];
          let block_dict={}
          for (let j = 0; j < block.children.length; j++) {
              
              if (block.children[j].id=="ingredient_image"){
                const image=block_dict["image"]=block.children[j].getAttribute("src");
                block_dict["image"]=image;
              }
              if (block.children[j].id=="name"){
                const name=block_dict["name"]=block.children[j].innerHTML;
                block_dict["name"]=name;
              }
              if (block.children[j].id=="amount"){
                const amount=block_dict["amount"]=block.children[j].innerHTML;
                block_dict["amount"]=amount;
              }
              if (block.children[j].id=="unit"){
                const unit=block_dict["unit"]=block.children[j].innerHTML;
                block_dict["unit"]=unit;
              }
          }
          ingredients.push(block_dict);
        } 
    
        const ingredient_image=document.querySelector("#ingredient_image").getAttribute("src");
        
        const instructions=document.querySelector("#instructions").textContent;
        
        const notes=document.querySelector("#notes").value;
    
        const recipe_info={"recipe_id": recipe_id, "title": title, "image": image, "time": time, "servings": servings, "calories": calories, "fat": fat, "protein": protein, "carbs": carbs, "dish_type": dish_type, "ingredients": ingredients, "instructions": instructions, "notes": notes, "meal_date": meal_date, "meal_category": meal_category};
    
        fetch('/save_to_meal_plan', {
            method: 'POST',
            body: JSON.stringify({recipe_info}),
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





