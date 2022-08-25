
gsap.fromTo("#context", 1, {x: "400"}, {x: '0%', ease: Power2.easeInOut});


const tl1 = new TimelineMax();

tl1.fromTo("#filter_buttons1", .5, {x: "-400"}, {x: '0%', ease: Power2.easeInOut}
).fromTo("#filter_buttons2", .5, {x: "-400"}, {x: '0%', ease: Power2.easeInOut}
).fromTo("#filter_buttons3", .5, {x: "-400"}, {x: '0%', ease: Power2.easeInOut}
).fromTo("#filter_buttons4", .5, {x: "-400"}, {x: '0%', ease: Power2.easeInOut}
).fromTo("#filter_buttons5", .5, {x: "-400"}, {x: '0%', ease: Power2.easeInOut}
).fromTo("#filter_buttons6", .5, {x: "-400"}, {x: '0%', ease: Power2.easeInOut}
).fromTo("#context_home", 1, {opacity: 0}, {opacity: 1, duration: 2});
