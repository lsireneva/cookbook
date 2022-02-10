document.querySelector("#del_favorites").addEventListener("click", evt => {
    evt.preventDefault();
    console.log('delete favorites pressed');

    const recipe_name = document.querySelector("#recipe_title").innerHTML;
    console.log(recipe_name);

    fetch('/delete_recipe_db', {
        method: 'POST',
        body: JSON.stringify({recipe_name}),
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then(response => response.json())
        .then(responseJson => {
          let myAlert = document.getElementById('recipeToast');
          let toastMessage = document.getElementById('toast_message');
          toastMessage.innerText="Deleted from favorites";
          let myToast = bootstrap.Toast.getOrCreateInstance(myAlert);
          myToast.show();         
        });


});