function tabSlider() {
	var $li1 = $('header li:nth-child(1)').outerWidth(),
		$li2 = $('header li:nth-child(2)').outerWidth(),
		$li3 = $('header li:nth-child(3)').outerWidth(),
		$li4 = $('header li:nth-child(4)').outerWidth(),
		$li5 = $('header li:nth-child(5)').outerWidth(),
		$li6 = $('header li:nth-child(6)').outerWidth();

	$color = $('.side-menu').find("li.active").css("background-color");

	if ($('header li:nth-child(2)').hasClass('active')) {
		$('.slider').css({
			'transform': 'translate(' + $li1 + 'px, 0)',
			'width': $li2,
			'background': $color
		});
	} else if ($('header li:nth-child(3)').hasClass('active')) {
		$('.slider').css({
			'transform': 'translate(' + ($li1 + $li2) + 'px, 0)',
			'width': $li3,
			'background': $color
		});
	} else if ($('header li:nth-child(4)').hasClass('active')) {
		$('.slider').css({
			'transform': 'translate(' + ($li1 + $li2 + $li3) + 'px, 0)',
			'width': $li4,
			'background': $color
		});
	} else if ($('header li:nth-child(5)').hasClass('active')) {
		$('.slider').css({
			'transform': 'translate(' + ($li1 + $li2 + $li3 + $li4) + 'px, 0)',
			'width': $li5,
			'background': $color
		});
	} else if ($('header li:nth-child(6)').hasClass('active')) {
		$('.slider').css({
			'transform': 'translate(' + ($li1 + $li2 + $li3 + $li4 + $li5) + 'px, 0)',
			'width': $li6,
			'background': $color
		});
	}
};

if (window.matchMedia("(max-width: 600px)").matches) {
  $('.similar').addClass('col-md-12');
} else {
  $('.similar .col-md-12').removeClass('col-md-12');
}

function cardHeight() {
	$('.card').each(function() {
		$(this).height($(this).width() + 56);
	});
};

function headerPadding() {
	var $headerHeight = $('header').outerHeight();
	$('main').css('padding-top', $headerHeight);
};

$(function() {
	"use strict";

	tabSlider();
	cardHeight();

	// TABS

	$('header li').on('click', function() {
		$('header li').removeClass('active');
		$(this).addClass('active');
		tabSlider();
	});

	// CARD HEIGHT & 'MAIN' PADDING

	$(window, 'main').resize(function() {
		cardHeight();
		headerPadding();
	}).resize();

	// HEADER SHADOW

	$(window).scroll(function() {
		if ($(this).scrollTop() >= 10) {
			$("header").addClass("shadow");
		} else {
			$("header").removeClass("shadow");
		}
	});

	// MENU

	$('.menu, .side-menu-overlay').on('click', function() {
		var $sidebarWidth = $('.side-menu').width();
		$('.side-menu').toggleClass('active');
		if ($('.side-menu').hasClass('active')) {
			$('header, main').css('width', 'calc(100% - ' + $sidebarWidth + 'px)');
			$('.categories').css('left', $sidebarWidth+5);
		} else {
			$('.categories').css('left', 5);
			$('header, main').css('width', '100%');
		}
	});

	// PROFILE MENU

	$('.profile').on('click', function() {
		$('.account').toggleClass('active');
	});

	$(document).on("click", function(e) {
		if (($(".account").hasClass("active")) && (!$(".account, .account *, .profile").is(e.target))) {
			$(".account").toggleClass("active");
		}
	});

	// Categories dropdown
	$('.dropdown').on('click', function() {
		$('.categories').toggleClass('active');
	});

	$('.dropdown').on("click", function(e) {
		if (($(".categories").hasClass("active")) && (!$(".categories, .categories *, .dropdown").is(e.target))) {
			$(".categories").toggleClass("active");
		}
	});

	// MOBILE SEARCH BUTTON

	$('label.mobile-only').on('click', function() {
		$(this).toggleClass('close');
		$('body').toggleClass('mobile-input');
	})

	// RIPPLE
  // CODE FROM HENDRY SADRAK'S PEN - https://codepen.io/hendrysadrak/pen/yNKZWO

	$(document).on('click', '.ripple', function(e) {

		var $ripple = $('<span class="rippling" />'),
			$button = $(this),
			btnOffset = $button.offset(),
			xPos = e.pageX - btnOffset.left,
			yPos = e.pageY - btnOffset.top,
			size = 0,
			animateSize = parseInt(Math.max($button.width(), $button.height()) * Math.PI);

		$ripple.css({
				top: yPos,
				left: xPos,
				width: size,
				height: size,
				backgroundColor: $button.attr("ripple-color"),
				opacity: $button.attr("ripple-opacity")
			})
			.appendTo($button)
			.animate({
				width: animateSize,
				height: animateSize,
				opacity: 0
			}, 500, function() {
				$(this).remove();
			});
	});

	// IOS STUFF

	if (navigator.userAgent.match(/(iPod|iPhone|iPad)/)) {
		$('body').addClass('ios');
	}

});
