/*! For license information please see loose-shells-cry.js.LICENSE.txt */
"use strict";(self.webpackChunk=self.webpackChunk||[]).push([[63],{63:(t,e,n)=>{n.d(e,{C:()=>s});var r=n(609),o=n(129),a=n.n(o);function i(t){return i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},i(t)}function c(){c=function(){return t};var t={},e=Object.prototype,n=e.hasOwnProperty,r=Object.defineProperty||function(t,e,n){t[e]=n.value},o="function"==typeof Symbol?Symbol:{},a=o.iterator||"@@iterator",l=o.asyncIterator||"@@asyncIterator",u=o.toStringTag||"@@toStringTag";function s(t,e,n){return Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{s({},"")}catch(t){s=function(t,e,n){return t[e]=n}}function f(t,e,n,o){var a=e&&e.prototype instanceof h?e:h,i=Object.create(a.prototype),c=new O(o||[]);return r(i,"_invoke",{value:E(t,n,c)}),i}function d(t,e,n){try{return{type:"normal",arg:t.call(e,n)}}catch(t){return{type:"throw",arg:t}}}t.wrap=f;var p={};function h(){}function v(){}function y(){}var b={};s(b,a,(function(){return this}));var m=Object.getPrototypeOf,g=m&&m(m(_([])));g&&g!==e&&n.call(g,a)&&(b=g);var w=y.prototype=h.prototype=Object.create(b);function x(t){["next","throw","return"].forEach((function(e){s(t,e,(function(t){return this._invoke(e,t)}))}))}function L(t,e){function o(r,a,c,l){var u=d(t[r],t,a);if("throw"!==u.type){var s=u.arg,f=s.value;return f&&"object"==i(f)&&n.call(f,"__await")?e.resolve(f.__await).then((function(t){o("next",t,c,l)}),(function(t){o("throw",t,c,l)})):e.resolve(f).then((function(t){s.value=t,c(s)}),(function(t){return o("throw",t,c,l)}))}l(u.arg)}var a;r(this,"_invoke",{value:function(t,n){function r(){return new e((function(e,r){o(t,n,e,r)}))}return a=a?a.then(r,r):r()}})}function E(t,e,n){var r="suspendedStart";return function(o,a){if("executing"===r)throw new Error("Generator is already running");if("completed"===r){if("throw"===o)throw a;return q()}for(n.method=o,n.arg=a;;){var i=n.delegate;if(i){var c=k(i,n);if(c){if(c===p)continue;return c}}if("next"===n.method)n.sent=n._sent=n.arg;else if("throw"===n.method){if("suspendedStart"===r)throw r="completed",n.arg;n.dispatchException(n.arg)}else"return"===n.method&&n.abrupt("return",n.arg);r="executing";var l=d(t,e,n);if("normal"===l.type){if(r=n.done?"completed":"suspendedYield",l.arg===p)continue;return{value:l.arg,done:n.done}}"throw"===l.type&&(r="completed",n.method="throw",n.arg=l.arg)}}}function k(t,e){var n=e.method,r=t.iterator[n];if(void 0===r)return e.delegate=null,"throw"===n&&t.iterator.return&&(e.method="return",e.arg=void 0,k(t,e),"throw"===e.method)||"return"!==n&&(e.method="throw",e.arg=new TypeError("The iterator does not provide a '"+n+"' method")),p;var o=d(r,t.iterator,e.arg);if("throw"===o.type)return e.method="throw",e.arg=o.arg,e.delegate=null,p;var a=o.arg;return a?a.done?(e[t.resultName]=a.value,e.next=t.nextLoc,"return"!==e.method&&(e.method="next",e.arg=void 0),e.delegate=null,p):a:(e.method="throw",e.arg=new TypeError("iterator result is not an object"),e.delegate=null,p)}function S(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function j(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function O(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(S,this),this.reset(!0)}function _(t){if(t){var e=t[a];if(e)return e.call(t);if("function"==typeof t.next)return t;if(!isNaN(t.length)){var r=-1,o=function e(){for(;++r<t.length;)if(n.call(t,r))return e.value=t[r],e.done=!1,e;return e.value=void 0,e.done=!0,e};return o.next=o}}return{next:q}}function q(){return{value:void 0,done:!0}}return v.prototype=y,r(w,"constructor",{value:y,configurable:!0}),r(y,"constructor",{value:v,configurable:!0}),v.displayName=s(y,u,"GeneratorFunction"),t.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===v||"GeneratorFunction"===(e.displayName||e.name))},t.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,y):(t.__proto__=y,s(t,u,"GeneratorFunction")),t.prototype=Object.create(w),t},t.awrap=function(t){return{__await:t}},x(L.prototype),s(L.prototype,l,(function(){return this})),t.AsyncIterator=L,t.async=function(e,n,r,o,a){void 0===a&&(a=Promise);var i=new L(f(e,n,r,o),a);return t.isGeneratorFunction(n)?i:i.next().then((function(t){return t.done?t.value:i.next()}))},x(w),s(w,u,"Generator"),s(w,a,(function(){return this})),s(w,"toString",(function(){return"[object Generator]"})),t.keys=function(t){var e=Object(t),n=[];for(var r in e)n.push(r);return n.reverse(),function t(){for(;n.length;){var r=n.pop();if(r in e)return t.value=r,t.done=!1,t}return t.done=!0,t}},t.values=_,O.prototype={constructor:O,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=void 0,this.done=!1,this.delegate=null,this.method="next",this.arg=void 0,this.tryEntries.forEach(j),!t)for(var e in this)"t"===e.charAt(0)&&n.call(this,e)&&!isNaN(+e.slice(1))&&(this[e]=void 0)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var e=this;function r(n,r){return i.type="throw",i.arg=t,e.next=n,r&&(e.method="next",e.arg=void 0),!!r}for(var o=this.tryEntries.length-1;o>=0;--o){var a=this.tryEntries[o],i=a.completion;if("root"===a.tryLoc)return r("end");if(a.tryLoc<=this.prev){var c=n.call(a,"catchLoc"),l=n.call(a,"finallyLoc");if(c&&l){if(this.prev<a.catchLoc)return r(a.catchLoc,!0);if(this.prev<a.finallyLoc)return r(a.finallyLoc)}else if(c){if(this.prev<a.catchLoc)return r(a.catchLoc,!0)}else{if(!l)throw new Error("try statement without catch or finally");if(this.prev<a.finallyLoc)return r(a.finallyLoc)}}}},abrupt:function(t,e){for(var r=this.tryEntries.length-1;r>=0;--r){var o=this.tryEntries[r];if(o.tryLoc<=this.prev&&n.call(o,"finallyLoc")&&this.prev<o.finallyLoc){var a=o;break}}a&&("break"===t||"continue"===t)&&a.tryLoc<=e&&e<=a.finallyLoc&&(a=null);var i=a?a.completion:{};return i.type=t,i.arg=e,a?(this.method="next",this.next=a.finallyLoc,p):this.complete(i)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),p},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var n=this.tryEntries[e];if(n.finallyLoc===t)return this.complete(n.completion,n.afterLoc),j(n),p}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var n=this.tryEntries[e];if(n.tryLoc===t){var r=n.completion;if("throw"===r.type){var o=r.arg;j(n)}return o}}throw new Error("illegal catch attempt")},delegateYield:function(t,e,n){return this.delegate={iterator:_(t),resultName:e,nextLoc:n},"next"===this.method&&(this.arg=void 0),p}},t}function l(t,e,n,r,o,a,i){try{var c=t[a](i),l=c.value}catch(t){return void n(t)}c.done?e(l):Promise.resolve(l).then(r,o)}function u(t){return function(){var e=this,n=arguments;return new Promise((function(r,o){var a=t.apply(e,n);function i(t){l(a,r,o,i,c,"next",t)}function c(t){l(a,r,o,i,c,"throw",t)}i(void 0)}))}}function s(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:void 0,n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:"Upload Picture",o=arguments.length>3&&void 0!==arguments[3]?arguments[3]:"Upload a new picture",i=arguments.length>4?arguments[4]:void 0,l=(0,r.rA)(n,o,!1,"success",f(t)),s=document.createElement("div");s.innerHTML=l,document.body.appendChild(s);var d=s.querySelector(".img-upload"),p=s.querySelector("#upload"),h=s.querySelector("#save"),v=s.querySelector("#cancel"),y=s.querySelector("#reset"),b=s.querySelector("#clear"),m=s.querySelector("#drag-mode-crop"),g=s.querySelector("#drag-mode-move"),w=s.querySelector("#flip-horizontal"),x=s.querySelector("#flip-vertical"),L=s.querySelector("#rotate-right"),E=s.querySelector("#rotate-left"),k=s.querySelector("#rotate-input"),S=new(a())(d,{aspectRatio:e,viewMode:1,responsive:!0,restore:!0,guides:!0,center:!0,highlight:!0,background:!0,movable:!0,rotatable:!0,scalable:!0,zoomable:!0,zoomOnWheel:!0,zoomOnTouch:!0,wheelZoomRatio:.1,cropBoxMovable:!0,cropBoxResizable:!0,toggleDragModeOnDblclick:!0});y.addEventListener("click",(function(){return S.reset()})),b.addEventListener("click",(function(){return S.clear()})),m.addEventListener("click",(function(){return S.setDragMode("crop")})),g.addEventListener("click",(function(){return S.setDragMode("move")})),w.addEventListener("click",(function(){return S.scaleX(-1*S.getData().scaleX)})),x.addEventListener("click",(function(){return S.scaleY(-1*S.getData().scaleY)})),L.addEventListener("click",(function(){S.rotate(90),k.value=S.getData().rotate.toString()})),E.addEventListener("click",(function(){S.rotate(-90),k.value=S.getData().rotate.toString()})),k.addEventListener("change",(function(){var t=parseInt(k.value,10)||0;S.rotateTo(t)})),p.addEventListener("click",u(c().mark((function t(){var e,n;return c().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:e=(0,r.ub)(p),(n=document.createElement("input")).type="file",n.accept="image/*",n.click(),n.addEventListener("change",u(c().mark((function t(){var o,a;return c().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if((o=n.files[0]).type.startsWith("image/")){t.next=4;break}return(0,r.Xj)("error","Oops!","The file you selected is not an image"),t.abrupt("return",e());case 4:e(),a=URL.createObjectURL(o),S.replace(a);case 7:case"end":return t.stop()}}),t)})))),e();case 6:case"end":return t.stop()}}),t)})))),h.addEventListener("click",u(c().mark((function t(){var e,n;return c().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return e=(0,r.ub)(h),t.next=3,i(S.getCroppedCanvas().toDataURL());case 3:n=t.sent,e(),n&&s.remove();case 6:case"end":return t.stop()}}),t)})))),v.addEventListener("click",(function(){return s.remove()}))}var f=function(t){return'\n<div class="w-100 d-flex justify-content-center gap-2">\n \x3c!-- Rotate +90 --\x3e\n <button \n id="rotate-right"\n class="button-slim w-100 btn btn-primary info loader-btn"\n loader-state=\'default\'> \n <p><i class="fa-solid fa-rotate-right"></i></p>\n </button>\n\n \x3c!-- Input --\x3e\n <input \n name="rotate-input"\n id="rotate-input" \n placeholder="0" \n value="0"\n class="form-control inp text-center">\n\n \x3c!-- Rotate -90 --\x3e\n <button \n id="rotate-left"\n class="button-slim w-100 btn btn-primary info loader-btn"\n loader-state=\'default\'> \n <p><i class="fa-solid fa-rotate-left"></i></p>\n </button>\n</div>\n\n<div class="w-100 d-flex justify-content-center gap-2 mb-2 mt-2">\n <img \n class="modal-body img-upload rounded"\n src="'.concat(t,'"\n alt="picture"\n >\n</div>\n\n\x3c!-- Other buttons --\x3e\n<div class="w-100 d-flex justify-content-center gap-3 mb-3">\n\n <div class="w-100 d-flex justify-content-center button-group">\n \x3c!-- Drag mode Crop --\x3e\n <button \n id="drag-mode-crop"\n class="button-slim w-100 btn btn-primary info loader-btn"\n loader-state=\'default\'> \n <p><i class="fa-solid fa-crop"></i></p>\n </button>\n\n \x3c!-- Drag mode Move --\x3e\n <button\n id="drag-mode-move"\n class="button-slim w-100 btn btn-primary info loader-btn"\n loader-state=\'default\'>\n <p><i class="fa-solid fa-up-down-left-right"></i></p>\n </button>\n </div>\n\n\n <div class="w-50 d-flex justify-content-center button-group">\n \x3c!-- Reset --\x3e\n <button \n id="reset"\n class="button-slim w-100 btn btn-warning warning loader-btn"\n loader-state=\'default\'> \n <p><i class="fa-solid fa-rotate"></i></p>\n </button>\n\n \x3c!-- Clear --\x3e\n <button \n id="clear"\n class="button-slim w-100 btn btn-warning warning loader-btn"\n loader-state=\'default\'> \n <p><i class="fa-solid fa-expand"></i></p>\n </button>\n </div>\n\n\n <div class="w-100 d-flex justify-content-center button-group">\n \x3c!-- Flip Horizontal --\x3e\n <button \n id="flip-horizontal"\n class="button-slim w-100 btn btn-primary info loader-btn"\n loader-state=\'default\'> \n <p><i class="fa-solid fa-arrows-left-right"></i></p>\n </button>\n\n \x3c!-- Flip Vertical --\x3e\n <button\n id="flip-vertical"\n class="button-slim w-100 btn btn-primary info loader-btn"\n loader-state=\'default\'>\n <p><i class="fa-solid fa-arrows-up-down"></i></p>\n </button>\n </div>\n\n</div>\n\n\n<div class="w-100 d-flex justify-content-center button-group">\n \x3c!-- Save --\x3e\n <button \n id="save"\n class="button-slim w-100 btn btn-success success loader-btn"\n loader-state=\'default\'> \n <p><i class="fa-solid fa-save"></i></p>\n </button>\n\n \x3c!-- Upload --\x3e\n <button\n id="upload"\n class="button-slim w-100 btn btn-primary info loader-btn"\n loader-state=\'default\'>\n <p><i class="fa-solid fa-upload"></i></p>\n </button>\n\n \x3c!-- Cancel --\x3e\n <button\n id="cancel"\n class="button-slim w-100 btn btn-danger error loader-btn"\n loader-state=\'default\'>\n <p><i class="fa-solid fa-times"></i></p>\n </button>\n</div>\n')}}}]);