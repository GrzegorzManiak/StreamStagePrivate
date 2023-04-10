/*! For license information please see grown-new-ancient.js.LICENSE.txt */
"use strict";(self.webpackChunk=self.webpackChunk||[]).push([[609,592],{609:(t,e,n)=>{function r(t){return r="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},r(t)}function o(){o=function(){return t};var t={},e=Object.prototype,n=e.hasOwnProperty,i=Object.defineProperty||function(t,e,n){t[e]=n.value},a="function"==typeof Symbol?Symbol:{},c=a.iterator||"@@iterator",s=a.asyncIterator||"@@asyncIterator",u=a.toStringTag||"@@toStringTag";function l(t,e,n){return Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{l({},"")}catch(t){l=function(t,e,n){return t[e]=n}}function f(t,e,n,r){var o=e&&e.prototype instanceof p?e:p,a=Object.create(o.prototype),c=new O(r||[]);return i(a,"_invoke",{value:k(t,n,c)}),a}function h(t,e,n){try{return{type:"normal",arg:t.call(e,n)}}catch(t){return{type:"throw",arg:t}}}t.wrap=f;var d={};function p(){}function v(){}function y(){}var m={};l(m,c,(function(){return this}));var g=Object.getPrototypeOf,x=g&&g(g(S([])));x&&x!==e&&n.call(x,c)&&(m=x);var b=y.prototype=p.prototype=Object.create(m);function w(t){["next","throw","return"].forEach((function(e){l(t,e,(function(t){return this._invoke(e,t)}))}))}function L(t,e){function o(i,a,c,s){var u=h(t[i],t,a);if("throw"!==u.type){var l=u.arg,f=l.value;return f&&"object"==r(f)&&n.call(f,"__await")?e.resolve(f.__await).then((function(t){o("next",t,c,s)}),(function(t){o("throw",t,c,s)})):e.resolve(f).then((function(t){l.value=t,c(l)}),(function(t){return o("throw",t,c,s)}))}s(u.arg)}var a;i(this,"_invoke",{value:function(t,n){function r(){return new e((function(e,r){o(t,n,e,r)}))}return a=a?a.then(r,r):r()}})}function k(t,e,n){var r="suspendedStart";return function(o,i){if("executing"===r)throw new Error("Generator is already running");if("completed"===r){if("throw"===o)throw i;return P()}for(n.method=o,n.arg=i;;){var a=n.delegate;if(a){var c=E(a,n);if(c){if(c===d)continue;return c}}if("next"===n.method)n.sent=n._sent=n.arg;else if("throw"===n.method){if("suspendedStart"===r)throw r="completed",n.arg;n.dispatchException(n.arg)}else"return"===n.method&&n.abrupt("return",n.arg);r="executing";var s=h(t,e,n);if("normal"===s.type){if(r=n.done?"completed":"suspendedYield",s.arg===d)continue;return{value:s.arg,done:n.done}}"throw"===s.type&&(r="completed",n.method="throw",n.arg=s.arg)}}}function E(t,e){var n=e.method,r=t.iterator[n];if(void 0===r)return e.delegate=null,"throw"===n&&t.iterator.return&&(e.method="return",e.arg=void 0,E(t,e),"throw"===e.method)||"return"!==n&&(e.method="throw",e.arg=new TypeError("The iterator does not provide a '"+n+"' method")),d;var o=h(r,t.iterator,e.arg);if("throw"===o.type)return e.method="throw",e.arg=o.arg,e.delegate=null,d;var i=o.arg;return i?i.done?(e[t.resultName]=i.value,e.next=t.nextLoc,"return"!==e.method&&(e.method="next",e.arg=void 0),e.delegate=null,d):i:(e.method="throw",e.arg=new TypeError("iterator result is not an object"),e.delegate=null,d)}function j(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function _(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function O(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(j,this),this.reset(!0)}function S(t){if(t){var e=t[c];if(e)return e.call(t);if("function"==typeof t.next)return t;if(!isNaN(t.length)){var r=-1,o=function e(){for(;++r<t.length;)if(n.call(t,r))return e.value=t[r],e.done=!1,e;return e.value=void 0,e.done=!0,e};return o.next=o}}return{next:P}}function P(){return{value:void 0,done:!0}}return v.prototype=y,i(b,"constructor",{value:y,configurable:!0}),i(y,"constructor",{value:v,configurable:!0}),v.displayName=l(y,u,"GeneratorFunction"),t.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===v||"GeneratorFunction"===(e.displayName||e.name))},t.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,y):(t.__proto__=y,l(t,u,"GeneratorFunction")),t.prototype=Object.create(b),t},t.awrap=function(t){return{__await:t}},w(L.prototype),l(L.prototype,s,(function(){return this})),t.AsyncIterator=L,t.async=function(e,n,r,o,i){void 0===i&&(i=Promise);var a=new L(f(e,n,r,o),i);return t.isGeneratorFunction(n)?a:a.next().then((function(t){return t.done?t.value:a.next()}))},w(b),l(b,u,"Generator"),l(b,c,(function(){return this})),l(b,"toString",(function(){return"[object Generator]"})),t.keys=function(t){var e=Object(t),n=[];for(var r in e)n.push(r);return n.reverse(),function t(){for(;n.length;){var r=n.pop();if(r in e)return t.value=r,t.done=!1,t}return t.done=!0,t}},t.values=S,O.prototype={constructor:O,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=void 0,this.done=!1,this.delegate=null,this.method="next",this.arg=void 0,this.tryEntries.forEach(_),!t)for(var e in this)"t"===e.charAt(0)&&n.call(this,e)&&!isNaN(+e.slice(1))&&(this[e]=void 0)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var e=this;function r(n,r){return a.type="throw",a.arg=t,e.next=n,r&&(e.method="next",e.arg=void 0),!!r}for(var o=this.tryEntries.length-1;o>=0;--o){var i=this.tryEntries[o],a=i.completion;if("root"===i.tryLoc)return r("end");if(i.tryLoc<=this.prev){var c=n.call(i,"catchLoc"),s=n.call(i,"finallyLoc");if(c&&s){if(this.prev<i.catchLoc)return r(i.catchLoc,!0);if(this.prev<i.finallyLoc)return r(i.finallyLoc)}else if(c){if(this.prev<i.catchLoc)return r(i.catchLoc,!0)}else{if(!s)throw new Error("try statement without catch or finally");if(this.prev<i.finallyLoc)return r(i.finallyLoc)}}}},abrupt:function(t,e){for(var r=this.tryEntries.length-1;r>=0;--r){var o=this.tryEntries[r];if(o.tryLoc<=this.prev&&n.call(o,"finallyLoc")&&this.prev<o.finallyLoc){var i=o;break}}i&&("break"===t||"continue"===t)&&i.tryLoc<=e&&e<=i.finallyLoc&&(i=null);var a=i?i.completion:{};return a.type=t,a.arg=e,i?(this.method="next",this.next=i.finallyLoc,d):this.complete(a)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),d},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var n=this.tryEntries[e];if(n.finallyLoc===t)return this.complete(n.completion,n.afterLoc),_(n),d}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var n=this.tryEntries[e];if(n.tryLoc===t){var r=n.completion;if("throw"===r.type){var o=r.arg;_(n)}return o}}throw new Error("illegal catch attempt")},delegateYield:function(t,e,n){return this.delegate={iterator:S(t),resultName:e,nextLoc:n},"next"===this.method&&(this.arg=void 0),d}},t}function i(t,e,n,r,o,i,a){try{var c=t[i](a),s=c.value}catch(t){return void n(t)}c.done?e(s):Promise.resolve(s).then(r,o)}function a(t){return function(){var e=this,n=arguments;return new Promise((function(r,o){var a=t.apply(e,n);function c(t){i(a,r,o,c,s,"next",t)}function s(t){i(a,r,o,c,s,"throw",t)}c(void 0)}))}}function c(t){return new Promise((function(e){return setTimeout(e,t)}))}function s(t){return t.disabled=!0,t.setAttribute("loader-state","hide-text"),function(){return new Promise(function(){var e=a(o().mark((function e(n){return o().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,c(1e3);case 2:t.setAttribute("loader-state","show-text"),t.disabled=!1,n();case 5:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}())}}function u(t,e,n,r){var o=arguments.length>4&&void 0!==arguments[4]?arguments[4]:"",i='\n \x3c!-- Continue --\x3e\n <button type="submit" class="btn yes btn-'.concat(r,' btn-lg w-75">\n Continue\n </button>\n\n \x3c!-- Continue --\x3e\n <button type="submit" class="btn no btn-danger btn-lg w-25 error">\n Cancel\n </button>\n ');return'\n <div\n style="z-index: 9999; position: fixed; top: 0; left: 0; width: 100vw;\n height: 100vh; background-color: rgba(0, 0, 0, 0.5);">\n\n <style>\n body {\n overflow: hidden!important;\n }\n </style>\n\n \n \x3c!-- Modal --\x3e\n <div class="modal d-flex justify-content-center align-items-center"\n style="z-index: 9999; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; \n background-color: rgba(0, 0, 0, 0.5);">\n\n \x3c!-- Modal content --\x3e\n <div \n class="modal-content bg-dark text-light rounded\n p-xxl-5 p-xl-5 p-lg-5 p-md-3 p-sm-3 p-2"\n style="width: 500px;"\n >\n\n \x3c!-- Header --\x3e\n <div class="mb-2 justify-content-start header">\n \x3c!-- Header --\x3e\n <h1 class="fw-bold ">'.concat(t,'</h1>\n\n \x3c!-- Descriptiopn --\x3e\n <p class="text-muted">').concat(e,'</p>\n </div>\n \n \x3c!-- Custom --\x3e\n <div class="d-flex justify-content-lg-start justify-content-center flex-column custom">\n ').concat(o||"",'\n </div>\n \n \x3c!-- Buttons --\x3e\n <div class="justify-content-lg-start justify-content-center d-flex buttons w-100 pop-up-buttons">\n ').concat(n?i:"","\n </div>\n </div>\n </div>\n </div>\n ")}n.d(e,{Xj:()=>l,rA:()=>u,ub:()=>s});var l=function(t,e,n){var r=arguments.length>3&&void 0!==arguments[3]?arguments[3]:5e3,o=arguments.length>4&&void 0!==arguments[4]?arguments[4]:function(){},i=document.getElementById("toasts");if(!i)throw new Error("No toasts element found");var a="\n <div \n toast-type='".concat(t,"'\n class='\n toast\n d-flex\n align-items-center\n justify-content-start\n '\n >\n \x3c!-- Icon, pinned to the top --\x3e\n <div class='toast-icon col-1'>\n <i class=\"fa-regular fa-circle-check\" icon='success'></i>\n <i class=\"fa-solid fa-triangle-exclamation\" icon='warning'></i>\n <i class=\"fa-solid fa-exclamation\" icon='error'></i>\n <i class=\"fa-solid fa-circle-info\" icon='info'></i>\n </div>\n\n \x3c!-- Content --\x3e\n <div class='toast-content col-9'>\n <p class='toast-content-header m-0'>").concat(e,"</p>\n <p class='toast-content-text m-0'>").concat(n,"</p>\n <p class='toast-content-time m-0'>Now</p>\n </div>\n\n \x3c!-- Close button --\x3e\n <div class='toast-close col-2'>\n <i class=\"fa-solid fa-times\"></i>\n </div>\n </div>\n "),c=document.createElement("div");c.innerHTML=a;var s=c.querySelector(".toast-close"),u=c.querySelector(".toast-content-time"),l=new Date,h=setInterval((function(){var t,e,n;u.innerText=(t=l,e=(Date.now()-t.getTime())/1e3,((n=[{threshold:0,label:"Just now"},{threshold:6e4,label:"A few seconds ago"},{threshold:36e5,label:"A few minutes ago"},{threshold:864e5,label:"A few hours ago"},{threshold:6048e5,label:"A few days ago"},{threshold:1/0,label:"A while ago"}]).find((function(t){var n=t.threshold;return e<=n}))||n[n.length-1]).label)}),1e3);s.addEventListener("click",(function(){f(c,i),clearInterval(h),o()})),setTimeout((function(){f(c,i),clearInterval(h),o()}),r),i.appendChild(c)};function f(t,e){return h.apply(this,arguments)}function h(){return(h=a(o().mark((function t(e,n){var r,i,a,s,u,l,f,h,d,p,v;return o().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:r=1e3,e.classList.add("toast-out"),i=e.children[0],a=getComputedStyle(i),s=a.getPropertyValue("margin-bottom"),u=e.offsetHeight+parseInt(s),l=n.children,f=Array.from(l).indexOf(e),e.style.animation&&(e.style.animation=""),h=0;case 8:if(!(h<l.length)){t.next=19;break}if(d=l[h],!(h<=f)){t.next=12;break}return t.abrupt("continue",16);case 12:if(!d.classList.contains("toast-out")){t.next=14;break}return t.abrupt("continue",16);case 14:d.style.setProperty("--toast-adjust-height","-".concat(u,"px")),d.style.animation="toast_adjust ".concat(r,"ms ease-in-out");case 16:h++,t.next=8;break;case 19:return t.next=21,c(r);case 21:e.classList.remove("toast-out"),p=0;case 23:if(!(p<l.length)){t.next=31;break}if(v=l[p],!(p<=f)){t.next=27;break}return t.abrupt("continue",28);case 27:v.style.animation="";case 28:p++,t.next=23;break;case 31:e.remove();case 32:case"end":return t.stop()}}),t)})))).apply(this,arguments)}}}]);