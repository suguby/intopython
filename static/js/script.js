$(document).ready(
    $(window).load(function(){

        // menu mobile
        $('.main-menu-toggle').click(function(e) {
            e.preventDefault();
            $('.main-menu-toggle').stop().toggleClass('opened');

            $('.main-menu-hidden').stop().toggle(function() {
                //$('.main-menu-toggle').toggleClass('opened');
            });
        });

        $('input,textarea').focus(function () {
            $(this).data('placeholder', $(this).attr('placeholder'))
                .attr('placeholder', '');
        }).blur(function () {
            $(this).attr('placeholder', $(this).data('placeholder'));
        });




        if($(window).innerWidth() <= 800) {
            var fixmeTop = $('.wrap_lesson-video').offset().top;       // get initial position of the element
            $(window).scroll(function() {                  // assign scroll event listener
                var currentScroll = $(window).scrollTop(); // get current position
                if (currentScroll >= fixmeTop) {           // apply position: fixed if you
                    $('.wrap_lesson-video').css({                      // scroll to that element or below it
                        position: 'fixed',
                        top: '15px',
                        paddingTop: '40px'
                    });
                    $('.description-lesson').css('margin-top','320px');
                } else {                                   // apply position: static
                    $('.wrap_lesson-video').css({                      // if you scroll above it
                        position: 'static'
                    });
                    $('.description-lesson').css('margin-top','0');
                }
                console.log(fixmeTop);
            });
        } else {
            var fixmeTop = $('.wrap_lesson-video').offset().top;       // get initial position of the element
            $(window).scroll(function() {                  // assign scroll event listener
                var currentScroll = $(window).scrollTop(); // get current position
                if (currentScroll >= fixmeTop) {           // apply position: fixed if you
                    $('.wrap_lesson-video').css({                      // scroll to that element or below it
                        position: 'fixed',
                        top: '66px'
                    });
                    $('.description-lesson').css('margin-top','320px');
                } else {                                   // apply position: static
                    $('.wrap_lesson-video').css({                      // if you scroll above it
                        position: 'static'
                    });
                    $('.description-lesson').css('margin-top','0');
                }
            });
        }
    })
);

