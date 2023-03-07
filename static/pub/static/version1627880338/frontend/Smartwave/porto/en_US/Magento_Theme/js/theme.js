/**
 * Copyright © 2015 Magento. All rights reserved.
 * See COPYING.txt for license details.
 */
require([
    'jquery',
    'mage/smart-keyboard-handler',
    'mage/mage',
    'mage/ie-class-fixer',
    'domReady!'
], function($, keyboardHandler) {
    'use strict';
    $(document).ready(function() {
        $('.cart-summary').mage('sticky', {
            container: '#maincontent'
        });

        $('.panel.header .header.links').clone().appendTo('#store\\.links');
    });
    keyboardHandler.apply();
});
require([
    'jquery'
], function($) {
    (function() {
        var ev = new $.Event('classadded'),
            orig = $.fn.addClass;
        $.fn.addClass = function() {
            $(this).trigger(ev, arguments);
            return orig.apply(this, arguments);
        }
    })();
    $.fn.extend({
        scrollToMe: function() {
            if ($(this).length) {
                var top = $(this).offset().top - 100;
                $('html,body').animate({
                    scrollTop: top
                }, 300);
            }
        },
        scrollToJustMe: function() {
            if ($(this).length) {
                var top = jQuery(this).offset().top;
                $('html,body').animate({
                    scrollTop: top
                }, 300);
            }
        }
    });
    $(document).ready(function() {
        var windowScroll_t;
        $(window).scroll(function() {
            clearTimeout(windowScroll_t);
            windowScroll_t = setTimeout(function() {
                if (jQuery(this).scrollTop() > 100) {
                    $('#totop').fadeIn();
                } else {
                    $('#totop').fadeOut();
                }
            }, 500);
        });
        $('#totop').off("click").on("click", function() {
            $('html, body').animate({
                scrollTop: 0
            }, 600);
        });
        if ($('body').hasClass('checkout-cart-index')) {
            if ($('#co-shipping-method-form .fieldset.rates').length > 0 && $('#co-shipping-method-form .fieldset.rates :checked').length === 0) {
                $('#block-shipping').on('collapsiblecreate', function() {
                    $('#block-shipping').collapsible('forceActivate');
                });
            }
        }
        $(".products-grid .weltpixel-quickview").each(function() {
            $(this).appendTo($(this).parent().parent().children(".product-item-photo"));
        });
        $(".word-rotate").each(function() {

            var $this = $(this),
                itemsWrapper = $(this).find(".word-rotate-items"),
                items = itemsWrapper.find("> span"),
                firstItem = items.eq(0),
                firstItemClone = firstItem.clone(),
                itemHeight = 0,
                currentItem = 1,
                currentTop = 0;

            itemHeight = firstItem.height();

            itemsWrapper.append(firstItemClone);

            $this
                .height(itemHeight)
                .addClass("active");

            setInterval(function() {
                currentTop = (currentItem * itemHeight);

                itemsWrapper.animate({
                    top: -(currentTop) + "px"
                }, 300, function() {
                    currentItem++;
                    if (currentItem > items.length) {
                        itemsWrapper.css("top", 0);
                        currentItem = 1;
                    }
                });

            }, 2000);

        });
        $(".top-links-icon").off("click").on("click", function(e) {
            if ($(this).parent().children("ul.links").hasClass("show")) {
                $(this).parent().children("ul.links").removeClass("show");
            } else {
                $(this).parent().children("ul.links").addClass("show");
            }
            e.stopPropagation();
        });
        $(".top-links-icon").parent().click(function(e) {
            e.stopPropagation();
        });
        $(".search-toggle-icon").click(function(e) {
            if ($(this).parent().children(".block-search").hasClass("show")) {
                $(this).parent().children(".block-search").removeClass("show");
                $(this).removeClass('open');
            } else {
                $(this).parent().children(".block-search").addClass("show");
                $(this).addClass('open');
            }
            e.stopPropagation();
        });
        $(".search-toggle-icon").parent().click(function(e) {
            e.stopPropagation();
        });
        $("html,body").click(function() {
            $(".search-toggle-icon").parent().children(".block-search").removeClass("show");
            $('.autocomplete-suggestions').hide();
            $(".search-toggle-icon").removeClass('open');
            $(".top-links-icon").parent().children("ul.links").removeClass("show");
        });

        /********************* Qty Holder **************************/
        $(document).on("click", ".qtyplus", function(e) {
            // Stop acting like a button
            e.preventDefault();
            // Get its current value
            var currentVal = parseInt($(this).parents('form').find('input[name="qty"]').val());
            // If is not undefined
            if (!isNaN(currentVal)) {
                // Increment
                $(this).parents('form').find('input[name="qty"]').val(currentVal + 1);
            } else {
                // Otherwise put a 0 there
                $(this).parents('form').find('input[name="qty"]').val(0);
            }
        });
        // This button will decrement the value till 0
        $(document).on("click", ".qtyminus", function(e) {
            // Stop acting like a button
            e.preventDefault();
            // Get the field name
            fieldName = $(this).attr('field');
            // Get its current value
            var currentVal = parseInt($(this).parents('form').find('input[name="qty"]').val());
            // If it isn't undefined or its greater than 0
            if (!isNaN(currentVal) && currentVal > 0) {
                // Decrement one
                $(this).parents('form').find('input[name="qty"]').val(currentVal - 1);
            } else {
                // Otherwise put a 0 there
                $(this).parents('form').find('input[name="qty"]').val(0);
            }
        });
        $(".qty-inc").unbind('click').click(function() {
            if ($(this).parents('.field.qty,.control.qty').find("input.input-text.qty").is(':enabled')) {
                $(this).parents('.field.qty,.control.qty').find("input.input-text.qty").val((+$(this).parents('.field.qty,.control.qty').find("input.input-text.qty").val() + 1) || 0);
                $(this).parents('.field.qty,.control.qty').find("input.input-text.qty").trigger('change');
                $(this).focus();
            }
        });
        $(".qty-dec").unbind('click').click(function() {
            if ($(this).parents('.field.qty,.control.qty').find("input.input-text.qty").is(':enabled')) {
                $(this).parents('.field.qty,.control.qty').find("input.input-text.qty").val(($(this).parents('.field.qty,.control.qty').find("input.input-text.qty").val() - 1 > 0) ? ($(this).parents('.field.qty,.control.qty').find("input.input-text.qty").val() - 1) : 0);
                $(this).parents('.field.qty,.control.qty').find("input.input-text.qty").trigger('change');
                $(this).focus();
            }
        });
    });
});
require([
    'jquery',
    'js/jquery.lazyload'
], function($) {
    $(document).ready(function() {
        $("img.porto-lazyload:not(.porto-lazyload-loaded)").lazyload({
            effect: "fadeIn"
        });
        if ($('.porto-lazyload:not(.porto-lazyload-loaded)').closest('.owl-carousel').length) {
            $('.porto-lazyload:not(.porto-lazyload-loaded)').closest('.owl-carousel').on('changed.owl.carousel', function() {
                $(this).find('.porto-lazyload:not(.porto-lazyload-loaded)').trigger('appear');
            });
            $('.porto-lazyload:not(.porto-lazyload-loaded)').closest('.owl-carousel').on('initialized.owl.carousel', function() {
                $(this).find('.porto-lazyload:not(.porto-lazyload-loaded)').trigger('appear');
            });
        }
        window.setTimeout(function() {
            $('.sidebar-filterproducts').find('.porto-lazyload:not(.porto-lazyload-loaded)').trigger('appear');
        }, 500);
    });
});