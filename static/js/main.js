$(document).ready(function() {

    //Enable Pagination
    window.recipe_index = $('.navbar-brand').attr('href');
    paginate(window);

    //Enable Tab Card for User Profile
    var current_url = window.location.pathname.split('/');
    if (current_url[1] == 'recipez' && current_url[2] == 'user_profile') {
        tabCardActivate();
    }

    if (current_url[1] == 'recipez' && current_url[2] == 'add_recipe') {
      var ingredientCounter = 0;
        $('#add-ingredient').click(function () {
            addNewIngredient(ingredientCounter);
        });
        $('#submit-ingredient').click(function () {
            submitIngredient(ingredientCounter);
        });
    }
    
  
    var scrollLink = $('.scroll');
    
    // Smooth scrolling
    scrollLink.click(function(e) {
      e.preventDefault();
      $('body,html').animate({
        scrollTop: $(this.hash).offset().top
      }, 1000 );
    });
    
    // Active link switching
    $(window).scroll(function() {
      var scrollbarLocation = $(this).scrollTop();
      
      scrollLink.each(function() {
        
        var sectionOffset = $(this.hash).offset().top - 20;
        
        if ( sectionOffset <= scrollbarLocation ) {
          $(this).parent().addClass('active');
          $(this).parent().siblings().removeClass('active');
        }
      })
      
    })

    var scrollButton = document.getElementById("btn-back-to-top");
    var topScrollPx = 50;

    window.onscroll = function () {
      scrollFunction();
    };

    function scrollFunction() {
      if (
        document.body.scrollTop > topScrollPx ||
        document.documentElement.scrollTop > topScrollPx
      ) {
        scrollButton.style.display = "block";
      } else {
        scrollButton.style.display = "none";
      }
    }
    
    // Function for user click to scroll to the top of the page
    scrollButton.addEventListener("click", backToTop);

    function backToTop() {
      document.body.scrollTop = 0;
      document.documentElement.scrollTop = 0;
      document.body.scrollIntoView({ behavior: "smooth" });
    }

    // Function for user click to close the alert
    $("#closeAlert").click(function() {
      $("#alert").hide();
    });

  })

  // Function of AJAX Pagination for Recipe Index
  function paginate(window) {
      var page = 1;
      var block_request = false;
      var end_pagination = false;

      $(window).scroll(function () {
          var margin = $(document).height() - $(window).height() - 300; // Saman told me to do this

          if ($(window).scrollTop() > margin && end_pagination === false && block_request === false) {
              block_request = true;
              page += 1;

              $.ajax({
                  type: 'GET',
                  url: window.recipe_index,
                  data: {
                      "page": page
                  },
                  success: function (data) {
                      if (data.end_pagination === true) {
                          end_pagination = true;
                      } else {
                          block_request = false;
                      }
                      $('.recipe-list').append(data.content);
                  }
              })
          }
      });
  }

  // Function of Tab Card for User Profile
  function tabCardActivate() {
    var nav_items1 = $('.nav-link.1');
    var tab_items1 = $('.tab-pane.1');

    $(nav_items1).click(function(){
        var id = $(this).attr('id');
        console.log(id);
        $(nav_items1).removeClass('active');
        $(this).addClass('active');
        $(tab_items1).removeClass('active');
        $(tab_items1).removeClass('show').addClass('fade');
        $('#'+id+'-post').addClass('active');
        $('#'+id+'-post').addClass('show');
    });
    
    var nav_items2 = $('.nav-link.2');
    var tab_items2 = $('.tab-pane.2');

    $(nav_items2).click(function(){
        var id = $(this).attr('id');
        console.log(id);
        $(nav_items2).removeClass('active');
        $(this).addClass('active');
        $(tab_items2).removeClass('active');
        $(tab_items2).removeClass('show');
        $('#'+id+'-saved').addClass('active');
        $('#'+id+'-saved').addClass('show');
    });
  }

  function addNewIngredient(ingredientCounter) {
    var ingredientForm = document.getElementById("ingredient-form");
    var newIngredientGroup = document.createElement("div");
    newIngredientGroup.setAttribute("class", "form-group");
    var newIngredientLabel = document.createElement("label");
    newIngredientLabel.innerHTML = "ingredient " + (++ingredientCounter);
    console.log(ingredientCounter);
    newIngredientGroup.appendChild(newIngredientLabel);
    var newIngredientInput = document.createElement("input");
    newIngredientInput.setAttribute("type", "text");
    newIngredientInput.setAttribute("name", "ingredient_set-" +
        (ingredientCounter - 1) + "-ingredient");
    newIngredientInput.setAttribute("class", "form-control");
    newIngredientGroup.appendChild(newIngredientInput);
    var newIngredientError = document.createElement("span");
    newIngredientError.setAttribute("style", "color: red");
    newIngredientGroup.appendChild(newIngredientError);
    ingredientForm.insertBefore(newIngredientGroup,
        ingredientForm.lastChild);
}

  function submitIngredient(ingredientCounter) {
      $('#id_ingredient_set-TOTAL_FORMS').attr("value", ingredientCounter.toString())
  }
  