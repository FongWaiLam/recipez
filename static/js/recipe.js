$(document).ready(function() {
    // Do something
});

var ingredientCounter = 0;
console.log(ingredientCounter);

function addNewIngredient() {
    ingredientCounter += 1;
    // Add the ingredient field
    $("#ingredient-form").append(
        '<div class="input-group p-3 mb-3">'+
        '<input type="text" placeholder="Ingredient" name="ingredient_set-' + (ingredientCounter - 1) + 
        '-ingredient" class="form-control"><span style="color: red;"></span>'+
        '<button class="close btn btn-danger" type="button" id="ingredient-close'+ingredientCounter+'"><span>x</span></button>' +
        '</div>');
    $('#id_ingredient_set-TOTAL_FORMS').attr("value", ingredientCounter.toString())

    // Remove the ingredient field
    $('#ingredient-close'+ingredientCounter).click(function() {
        $('#ingredient-close'+ingredientCounter).parent().remove();
        ingredientCounter -= 1;
        $('#id_ingredient_set-TOTAL_FORMS').attr("value", ingredientCounter.toString())
    });
}