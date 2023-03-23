$(document).ready(function() {
    let cookie = document.cookie
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    // Do something
    var ifLiked = $("#likeButton").attr('if-liked');
    var likeLink = $("#likeButton").attr('link');
    var user = $("#likeButton").attr('user');
    var recipe = $("#likeButton").attr('recipe-id');

    console.log(ifLiked)
    checkUpdateLike();

    var likeClick = function() {
        var ifLiked = $("#likeButton").attr('if-liked');
        if (ifLiked == "False") {
            $.ajax({
                type: 'POST',
                url: likeLink,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                data: {
                    'user': user,
                    'recipe': recipe,
                },
                success: function(data) {
                    $("#like-counter").text(data.likes);
                    $("#likeButton").attr('if-liked', "True");
                    ifLiked = checkUpdateLike(); 
                    console.log("Success on like");
                },
                error: function() {
                    $("#like-counter").text(data.likes);
                    console.log("Error on like");
                }
            });
        }   else if (ifLiked == "True") {
            $.ajax({
                type: 'POST',
                url: likeLink,
                headers: {
                    'X-CSRFToken': csrfToken
                },
                data: {
                    'user': user,
                    'recipe': recipe,
                },
                success: function(data) {
                    $("#like-counter").text(data.likes);
                    $("#likeButton").attr('if-liked', "False");
                    ifLiked = checkUpdateLike(); 
                    console.log("Success on unlike");
                },
                error: function() {
                    $("#like-counter").text(data.likes);
                    console.log("Error on unlike");
                }
            });
        }  
    }
    $("#likeButton").on("click", likeClick);

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

function copyUrl() {
    navigator.clipboard.writeText(this.location.href);
    alert("Copied to clipboard!");
}

function checkUpdateLike() {
    var ifLiked = $("#likeButton").attr('if-liked');
    if (ifLiked == "True") {
        $("#heart").hide();
        $("#heart-fill").show();
    } else {
        $("#heart-fill").hide();
        $("#heart").show();
    }
    return ifLiked;
}