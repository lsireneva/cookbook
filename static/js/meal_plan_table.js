"use strict";
function deleteRecipe(element, recipe_name) {
    console.log("delete pressed")
    fetch('/delete_recipe_from_mealplan', {
        method: 'POST',
        body: JSON.stringify({recipe_name}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseJson => {
        const recipe_name_element = element.parentElement;
        recipe_name_element.remove();
    })
}