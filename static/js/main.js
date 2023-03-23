$(document).ready(function() {

    //Enable Pagination
    window.recipe_index = $('.navbar-brand').attr('href');
    paginate(window);
    
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



  