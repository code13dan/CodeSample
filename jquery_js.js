
$(function(){
    // ######## this is raw copy for testing purpose
    console.log('new navbar on');
    var old_navbar = $('nav.navbar'),
        new_navbar = old_navbar.clone();

    // ############### Megamenu ####################

    // ##get megamenu and copy it
    megamenu_li_small = new_navbar.find('li.dropdown.yamm-fw')

    // ##transform megamenu copy for small screens

    // editing classes of li and it's main ul
    megamenu_ul_small = megamenu_li_small.find( 'ul.dropdown-menu' );

    // converting submenus
    new_submenu_li = $("\
    <li>\
        <a href='javascript:void(0)' class='has_children'></a>\
        <ul class='dropdown-menu-left'>\
        </ul>\
    </li>\
    ");
    submenus_main = megamenu_li_small.find( 'h3.megamenu-block-title' );
    megamenu_ul_small.empty();
    submenus_main.each(function(){
        // get elements to transform
        submenu_li_text = $( this ).text();
        submenu_menu_a = $( this ).next('ul').find('a');
        template = new_submenu_li.clone();

        // insert transformed elements content to new elements
        template.children('a').text(submenu_li_text);
        submenu_menu_a.each(function(){
            ul_to_append = template.find('ul');
            $( this ).find('i').remove();
            $( this ).attr('class','sub_navs_a');
            $( this ).appendTo(ul_to_append);
            $( this ).wrap("<li></li>")
        });

        // insert new elements
        template.appendTo(megamenu_ul_small);
    });


    // changing important classes and ids
    new_navbar.find('#navbarContainer').removeAttr('class').attr('id','navbar-container');
    new_navbar.find('#navbar').attr('id','navbar-min').removeAttr('class');
    new_navbar.find('ul,li,a').removeAttr('class').removeAttr('data-toggle').removeAttr('data-hover');
    new_navbar.removeAttr('class').addClass('nav-navbar');


    // create and add trigger for dropdown
    trigger = $('<div id="trigger-collapse" class="text-center"><i style="font-size:20px" class="zmdi zmdi-menu"></i></div>');
    trigger.prependTo(new_navbar.find('#navbar-container'));


    // ######### Small screen navbar trigger action ####
    new_navbar.find( '#trigger-collapse' ).on('click.collapse',function(){
        if ( $( '#navbar-min' ).css('display') == 'none') {
            $( '#navbar-min' ).attr('style','display:block');

        } else {
            $( '#navbar-min' ).attr('style','display:none');
        };
    });

    // ####### Show ul ##########
    new_navbar.find('#navbar-min > ul a').on('click.subdrop', function(e){
        e.preventDefault();
        $( this ).parent('li').siblings('li').removeClass('drop');
        $( this ).parent('li').siblings('li').find('li.drop').removeClass('drop');
        $( this ).parent('li').toggleClass('drop');
        return false
    });


    // class changing
    new_navbar.find('#navbar-min > ul > li > ul').addClass('menu');
    new_navbar.find('.menu ul').addClass('submenu');
    new_navbar.find('.zmdi-chevron-down').removeClass('zmdi-chevron-down').addClass('zmdi-chevron-left');

    // add it all
    new_navbar.insertAfter(old_navbar);
});
