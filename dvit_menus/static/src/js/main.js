function dvit() {
'use strict';
$(document).ready(function(){
    $('.cssmenu').hover(function () {
        if(!$(this).find('h3').hasClass('fix_active')) {
            $(this).find('h3').addClass('active');
            $(this).find('div.oe_secondary_menu').css("height", "initial");
            $(this).find('div.oe_secondary_menu').stop().slideDown('slow');
        }
        },function () {
        if(!$(this).find('h3').hasClass('fix_active')) {
            $(this).find('h3').removeClass('active');
            $(this).find('div.oe_secondary_menu').css("height", "initial");
            $(this).find('div.oe_secondary_menu').stop().slideUp('slow');
        }
    });
    
    $('.cssmenu > h3').click(function() {
        if( $( this ).hasClass('fix_active') ){
            $( this ).removeClass('fix_active');
            $(this).find('div.oe_secondary_menu').css("height", "initial");
            $(this).parent().find('div.oe_secondary_menu').stop().slideUp('slow');
        } else {
            $(this).find('div.oe_secondary_menu').css("height", "initial");
            $( this ).addClass('fix_active');
        }
    });

    $('.cssmenu .oe_menu_toggler').click(function() {
        $('.cssmenu .oe_menu_toggler').removeClass('active');
        $(this).closest('.oe_menu_toggler').addClass('active');
        // var checkElement = $(this).next();
        // if((checkElement.is('.oe_secondary_submenu')) && (checkElement.is(':visible'))) {
        //     $(this).closest('.oe_menu_toggler').removeClass('active');
        //     checkElement.slideUp(100);
        // }
        // if((checkElement.is('.oe_secondary_submenu')) && (!checkElement.is(':visible'))) {
        //     $('#cssmenu .oe_menu_toggler:visible').slideUp(100);
        //     checkElement.slideDown(100);
        // }
    });
    
    $('.oe_secondary_submenu li a.oe_menu_leaf').click(function() {
        $('.oe_secondary_submenu li').removeClass('active');
        $(this).parent().addClass('active');
    });


});

    openerp.web.Client.include({
        bind_events: function () {
            var self = this;
            this._super();

            var root = self.$el;
            var elem_sm = $("<a><i class='fa fa-bars'></i></a>");
            elem_sm.appendTo(root.find('.menu-toogle'));

            self.$el.on('click', '.leftbar_toggle', function () {
                var leftbar = root.find('.oe_leftbar > div');
                if (leftbar.hasClass('fix_icon_width')) {
                    leftbar.removeClass('fix_icon_width');
                    leftbar.parent().removeClass('fix_icon_width');
                    leftbar.find('.menu_title').show();
                    leftbar.find('.oe_logo').show();
                    leftbar.find('.oe_footer').show();
                    leftbar.find('#dvit_space').hide();
                } else {
                    $('h3.menu_heading').removeClass('fix_active');
                    $('h3.menu_heading').parent().find('div.oe_secondary_menu').stop().slideUp(500);
                    leftbar.find('.menu_title').hide();
                    leftbar.find('.oe_footer').hide();
                    leftbar.addClass('fix_icon_width');
                    leftbar.parent().addClass('fix_icon_width');
                    leftbar.find('.oe_logo').hide();
                    leftbar.find('#dvit_space').show();
                }
            });
        }
    });
}

dvit();












