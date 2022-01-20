"use strict";


document.querySelector("#add_favorites").addEventListener("click", evt => {
    evt.preventDefault();
    console.log('add favorites pressed');
    
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

    const dish_type = document.querySelector("#dish_type").innerHTML;
    console.log(dish_type);
    
    //const ingredients=document.querySelector("#ingredients").textContent;
    //console.log(document.querySelector("#ingredients"))
    //console.log(ingredients);
    const ingredients = []
    const item=document.querySelectorAll("#item");
    for (let i = 0; i < item.length; i++) {
      
      let block=item[i];
      let block_dict={}
      for (let j = 0; j < block.children.length; j++) {
          
          if (block.children[j].id=="ingredient_image"){
            const image=block_dict["image"]=block.children[j].getAttribute("src");
            console.log(block.children[j].getAttribute("src"));
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
        console.log(block_dict);  
      }
      ingredients.push(block_dict);
    } 
    console.log(ingredients);
    //console.log(document.querySelectorAll("#item"))

    const ingredient_image=document.querySelector("#ingredient_image").getAttribute("src");
    //console.log(document.querySelector("#ingredient_image"))
    //console.log(ingredient_image);

    const instructions=document.querySelector("#instructions").textContent;
    //console.log(document.querySelector("#instructions"))
    //console.log(instructions);
    
    const notes=document.querySelector("#notes").value;
    //console.log(notes)

    const recipe_info={"recipe_id": recipe_id, "title": title, "image": image, "time": time, "servings": servings, "calories": calories, "fat": fat, "protein": protein, "carbs": carbs, "dish_type": dish_type, "ingredients": ingredients, "instructions": instructions, "notes": notes};
    //console.log(recipe_info);

    fetch('/save_recipe_to_db', {
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


});