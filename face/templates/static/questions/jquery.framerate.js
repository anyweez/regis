/*
 * jQuery Framerate 1.0.1
 *
 ** IMPORTANT: THIS HAS ONLY BEEN TESTED WITH JQUERY 1.4.2.  SINCE THIS PLUGIN MODIFIES PARTS OF THE
 ** CORE CODE, IT MAY NOT WORK CORRECTLY IN OTHER VERSIONS. LET ME KNOW IF YOU FIND ANOTHER
 ** VERSION IT DOESN'T WORK IN AND I'LL SEE IF I CAN MODIFY TO WORK WITH IT
 *
 *
 * Summary:
 * Override some of the core code of JQuery to allow for custom framerates
 * The default framerate is very high (@77fps) and can therefore lead to choppy motion on
 * complicated animations on slower machines
 *
 * Usage:
 * takes two parameters, one for desired framerate (default of 30) and other to display
 * framerate in console while animation is running.
 *
 * example basic usage: $().framerate();
 * example advanced usage: $().framerate({framerate: 20, logframes: true});
 *
 *
 *
 * TERMS OF USE - jQuery Framerate
 *
 * Copyright © 2010 James Snodgrass: jim@skookum.com
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification, 
 * are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice, this list of 
 * conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice, this list 
 * of conditions and the following disclaimer in the documentation and/or other materials 
 * provided with the distribution.
 * 
 * Neither the name of the author nor the names of contributors may be used to endorse 
 * or promote products derived from this software without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
 * GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED 
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED 
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 *
 * Changes:
 * 1.0.1: July 30,2010 - fixed global variable leaks
 *
*/


jQuery.fn.framerate = function(options) {


var settings = jQuery.extend({
   framerate: 30,
   logframes: false
}, options);

var frameInterval = Math.floor(1000/settings.framerate);

jQuery.extend( jQuery.fx.prototype, {
	// Start an animation from one number to another
	custom: function( from, to, unit ) {
		this.startTime = new Date().getTime();
		this.start = from;
		this.end = to;
		this.unit = unit || this.unit || "px";
		this.now = this.start;
		this.pos = this.state = 0;

		var self = this;
		function t( gotoEnd ) {
			return self.step(gotoEnd);
		}

		t.elem = this.elem;
		
		if (typeof(jQuery.timerId) == 'undefined') jQuery.timerId = false;
		
		if ( t() && jQuery.timers.push(t) && !jQuery.timerId ) {
			jQuery.timerId = setInterval(jQuery.fx.tick, frameInterval);
		}
	}
});

var lastTimeStamp = new Date().getTime();  

jQuery.extend( jQuery.fx, {
	tick: function() {
		
		if (settings.logframes) {
			var now = new Date().getTime();
			console.log(Math.floor(1000/(now - lastTimeStamp))); 
    		lastTimeStamp = now;
		}
		 
		
		var timers = jQuery.timers;
		
		for ( var i = 0; i < timers.length; i++ ) {
			if ( !timers[i]() ) {
				timers.splice(i--, 1);
			}
		}

		if ( !timers.length ) {
			jQuery.fx.stop();
		}
	},
	stop: function() {
		clearInterval( jQuery.timerId );
		jQuery.timerId = null;
	}
});

}
