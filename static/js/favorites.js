"use strict";


document.querySelector("#add_favorites").addEventListener("click", evt => {
    evt.preventDefault();
    console.log('add favorites pressed');
    
    const title = document.querySelector("#recipe_title").innerHTML;
    console.log(title);
    
    const image=document.querySelector("#recipe_image").getAttribute("src");
    console.log(image);
    const time = document.querySelector("#time").innerHTML;
    console.log(time);
    const servings = document.querySelector("#servings").innerHTML;
    console.log(servings);
    const calories = document.querySelector("#calories").innerHTML;
    console.log(calories);
    const fat = document.querySelector("#fat").innerHTML;
    console.log(fat);
    const protein = document.querySelector("#protein").innerHTML;
    console.log(protein);
    const carbs = document.querySelector("#carbs").innerHTML;
    console.log(carbs);
    
    const ingredients=document.querySelector("#ingredients").textContent;
    console.log(document.querySelector("#ingredients"))
    console.log(ingredients);

    const instructions=document.querySelector("#instructions").textContent;
    console.log(document.querySelector("#instructions"))
    console.log(instructions);
    
    const notes=document.querySelector("#notes").value;
    console.log(notes)

    const recipe_info={"title": title, "image": image, "time": time, "servings": servings, "calories": calories, "fat": fat, "protein": protein, "carbs": carbs, "ingredients": ingredients, "instructions": instructions, "notes": notes};
    console.log(recipe_info);

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