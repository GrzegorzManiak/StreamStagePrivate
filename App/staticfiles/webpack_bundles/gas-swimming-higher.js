/*! For license information please see gas-swimming-higher.js.LICENSE.txt */
"use strict";(self.webpackChunk=self.webpackChunk||[]).push([[685],{881:(t,e,r)=>{r.d(e,{DN:()=>I,Is:()=>Y});var n=r(407),o=r(724),i=r(609),a=r(440);function u(t){return u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},u(t)}function c(){c=function(){return t};var t={},e=Object.prototype,r=e.hasOwnProperty,n=Object.defineProperty||function(t,e,r){t[e]=r.value},o="function"==typeof Symbol?Symbol:{},i=o.iterator||"@@iterator",a=o.asyncIterator||"@@asyncIterator",s=o.toStringTag||"@@toStringTag";function l(t,e,r){return Object.defineProperty(t,e,{value:r,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{l({},"")}catch(t){l=function(t,e,r){return t[e]=r}}function f(t,e,r,o){var i=e&&e.prototype instanceof d?e:d,a=Object.create(i.prototype),u=new S(o||[]);return n(a,"_invoke",{value:E(t,r,u)}),a}function h(t,e,r){try{return{type:"normal",arg:t.call(e,r)}}catch(t){return{type:"throw",arg:t}}}t.wrap=f;var p={};function d(){}function v(){}function y(){}var g={};l(g,i,(function(){return this}));var m=Object.getPrototypeOf,w=m&&m(m(j([])));w&&w!==e&&r.call(w,i)&&(g=w);var b=y.prototype=d.prototype=Object.create(g);function x(t){["next","throw","return"].forEach((function(e){l(t,e,(function(t){return this._invoke(e,t)}))}))}function L(t,e){function o(n,i,a,c){var s=h(t[n],t,i);if("throw"!==s.type){var l=s.arg,f=l.value;return f&&"object"==u(f)&&r.call(f,"__await")?e.resolve(f.__await).then((function(t){o("next",t,a,c)}),(function(t){o("throw",t,a,c)})):e.resolve(f).then((function(t){l.value=t,a(l)}),(function(t){return o("throw",t,a,c)}))}c(s.arg)}var i;n(this,"_invoke",{value:function(t,r){function n(){return new e((function(e,n){o(t,r,e,n)}))}return i=i?i.then(n,n):n()}})}function E(t,e,r){var n="suspendedStart";return function(o,i){if("executing"===n)throw new Error("Generator is already running");if("completed"===n){if("throw"===o)throw i;return P()}for(r.method=o,r.arg=i;;){var a=r.delegate;if(a){var u=k(a,r);if(u){if(u===p)continue;return u}}if("next"===r.method)r.sent=r._sent=r.arg;else if("throw"===r.method){if("suspendedStart"===n)throw n="completed",r.arg;r.dispatchException(r.arg)}else"return"===r.method&&r.abrupt("return",r.arg);n="executing";var c=h(t,e,r);if("normal"===c.type){if(n=r.done?"completed":"suspendedYield",c.arg===p)continue;return{value:c.arg,done:r.done}}"throw"===c.type&&(n="completed",r.method="throw",r.arg=c.arg)}}}function k(t,e){var r=e.method,n=t.iterator[r];if(void 0===n)return e.delegate=null,"throw"===r&&t.iterator.return&&(e.method="return",e.arg=void 0,k(t,e),"throw"===e.method)||"return"!==r&&(e.method="throw",e.arg=new TypeError("The iterator does not provide a '"+r+"' method")),p;var o=h(n,t.iterator,e.arg);if("throw"===o.type)return e.method="throw",e.arg=o.arg,e.delegate=null,p;var i=o.arg;return i?i.done?(e[t.resultName]=i.value,e.next=t.nextLoc,"return"!==e.method&&(e.method="next",e.arg=void 0),e.delegate=null,p):i:(e.method="throw",e.arg=new TypeError("iterator result is not an object"),e.delegate=null,p)}function _(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function O(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function S(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(_,this),this.reset(!0)}function j(t){if(t){var e=t[i];if(e)return e.call(t);if("function"==typeof t.next)return t;if(!isNaN(t.length)){var n=-1,o=function e(){for(;++n<t.length;)if(r.call(t,n))return e.value=t[n],e.done=!1,e;return e.value=void 0,e.done=!0,e};return o.next=o}}return{next:P}}function P(){return{value:void 0,done:!0}}return v.prototype=y,n(b,"constructor",{value:y,configurable:!0}),n(y,"constructor",{value:v,configurable:!0}),v.displayName=l(y,s,"GeneratorFunction"),t.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===v||"GeneratorFunction"===(e.displayName||e.name))},t.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,y):(t.__proto__=y,l(t,s,"GeneratorFunction")),t.prototype=Object.create(b),t},t.awrap=function(t){return{__await:t}},x(L.prototype),l(L.prototype,a,(function(){return this})),t.AsyncIterator=L,t.async=function(e,r,n,o,i){void 0===i&&(i=Promise);var a=new L(f(e,r,n,o),i);return t.isGeneratorFunction(r)?a:a.next().then((function(t){return t.done?t.value:a.next()}))},x(b),l(b,s,"Generator"),l(b,i,(function(){return this})),l(b,"toString",(function(){return"[object Generator]"})),t.keys=function(t){var e=Object(t),r=[];for(var n in e)r.push(n);return r.reverse(),function t(){for(;r.length;){var n=r.pop();if(n in e)return t.value=n,t.done=!1,t}return t.done=!0,t}},t.values=j,S.prototype={constructor:S,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=void 0,this.done=!1,this.delegate=null,this.method="next",this.arg=void 0,this.tryEntries.forEach(O),!t)for(var e in this)"t"===e.charAt(0)&&r.call(this,e)&&!isNaN(+e.slice(1))&&(this[e]=void 0)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var e=this;function n(r,n){return a.type="throw",a.arg=t,e.next=r,n&&(e.method="next",e.arg=void 0),!!n}for(var o=this.tryEntries.length-1;o>=0;--o){var i=this.tryEntries[o],a=i.completion;if("root"===i.tryLoc)return n("end");if(i.tryLoc<=this.prev){var u=r.call(i,"catchLoc"),c=r.call(i,"finallyLoc");if(u&&c){if(this.prev<i.catchLoc)return n(i.catchLoc,!0);if(this.prev<i.finallyLoc)return n(i.finallyLoc)}else if(u){if(this.prev<i.catchLoc)return n(i.catchLoc,!0)}else{if(!c)throw new Error("try statement without catch or finally");if(this.prev<i.finallyLoc)return n(i.finallyLoc)}}}},abrupt:function(t,e){for(var n=this.tryEntries.length-1;n>=0;--n){var o=this.tryEntries[n];if(o.tryLoc<=this.prev&&r.call(o,"finallyLoc")&&this.prev<o.finallyLoc){var i=o;break}}i&&("break"===t||"continue"===t)&&i.tryLoc<=e&&e<=i.finallyLoc&&(i=null);var a=i?i.completion:{};return a.type=t,a.arg=e,i?(this.method="next",this.next=i.finallyLoc,p):this.complete(a)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),p},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.finallyLoc===t)return this.complete(r.completion,r.afterLoc),O(r),p}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.tryLoc===t){var n=r.completion;if("throw"===n.type){var o=n.arg;O(r)}return o}}throw new Error("illegal catch attempt")},delegateYield:function(t,e,r){return this.delegate={iterator:j(t),resultName:e,nextLoc:r},"next"===this.method&&(this.arg=void 0),p}},t}function s(t,e,r,n,o,i,a){try{var u=t[i](a),c=u.value}catch(t){return void r(t)}u.done?e(c):Promise.resolve(c).then(n,o)}function l(t){return function(){var e=this,r=arguments;return new Promise((function(n,o){var i=t.apply(e,r);function a(t){s(i,n,o,a,u,"next",t)}function u(t){s(i,n,o,a,u,"throw",t)}a(void 0)}))}}function f(t,e,r,n){return h.apply(this,arguments)}function h(){return(h=l(c().mark((function t(e,r,n,o){var u,s,f,h;return c().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:u=document.querySelector(".clock"),s=document.querySelector("#email-resend-btn"),f=900,h=setInterval((function(){f-=1;var t=Math.floor(f/60),e=f%60<10?"0".concat(f%60):f%60;u.innerText="".concat(t,":").concat(e),f<=0&&(clearInterval(h),u.innerText="0:00",s.disabled=!0,Y("login"),(0,i.Xj)("warning","Authentication","The verification code has expired"))}),1e3),(0,a.gW)((function(){return r})).then(l(c().mark((function t(){return c().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,new Promise((function(){return setTimeout((function(){window.location.href="/"}),3e3)}));case 2:case"end":return t.stop()}}),t)})))),e.addEventListener("click",l(c().mark((function t(){var u,s,l;return c().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return u=(0,i.ub)(e),t.next=3,(0,a.s1)(n,o());case 3:if(200===(s=t.sent).code){t.next=7;break}return(0,i.Xj)("error","Authentication","Failed to resend the verification code"),t.abrupt("return",u());case 7:(0,i.Xj)("success","Authentication","The verification code has been resent"),l=s.data,r=l.verify,n=l.token,f=54e3,u();case 13:case"end":return t.stop()}}),t)}))));case 5:case"end":return t.stop()}}),t)})))).apply(this,arguments)}var p=function(t){var e=[];return(t.length<8||t.length>64)&&e.push("length"),t.match(/\d/)||e.push("number"),t.match(/[A-Z]/)||e.push("uppercase"),t.match(/[a-z]/)||e.push("lowercase"),t.match(/\s/)&&e.push("spaces"),e},d=function(t){var e=[];return(t.length<3||t.length>20)&&e.push("length"),t.match(/^[a-zA-Z]/)||e.push("start"),t.match(/^\w+$/)||e.push("characters"),t.match(/__+/)&&e.push("double-underscore"),t.match(/_$/)&&e.push("end-underscore"),e},v=function(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:null;null===e&&(e=t);var r=function(){var r=p(t.value);return r.forEach((function(t){e.setAttribute("data-error-".concat(t),"")})),["length","number","uppercase","lowercase","spaces"].forEach((function(t){r.includes(t)||e.removeAttribute("data-error-".concat(t))})),0===r.length?"3":1===r.length?"2":2===r.length?"1":3===r.length||4===r.length?"0":void 0};t.addEventListener("keyup",(function(){t.setAttribute("data-strength",r())})),t.addEventListener("blur",(function(){e.removeAttribute("data-strength")})),t.addEventListener("focus",(function(){e.setAttribute("data-strength",r())})),t.addEventListener("input",(function(){t.value.length>0&&t.setAttribute("data-strength",r())}))},y=function(t){var e=function(){var e=d(t.value);if(e.forEach((function(e){t.setAttribute("data-error-".concat(e),"")})),["length","start","characters","double-underscore","end-underscore"].forEach((function(r){e.includes(r)||t.removeAttribute("data-error-".concat(r))})),0===e.length)return"3"};t.addEventListener("keyup",(function(){t.setAttribute("data-strength",e())})),t.addEventListener("blur",(function(){t.removeAttribute("data-strength")})),t.addEventListener("focus",(function(){t.setAttribute("data-strength",e())})),t.addEventListener("input",(function(){t.value.length>0&&t.setAttribute("data-strength",e())}))},g=function(t,e){var r=function(){return t.value===e.value?(e.setAttribute("data-strength","3"),!0):(e.setAttribute("data-strength","0"),!1)};e.addEventListener("keyup",(function(){r()})),e.addEventListener("blur",(function(){e.removeAttribute("data-strength")})),e.addEventListener("focus",(function(){r()})),e.addEventListener("input",(function(){e.value.length>0&&r()}))};function m(t){return m="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},m(t)}function w(){w=function(){return t};var t={},e=Object.prototype,r=e.hasOwnProperty,n=Object.defineProperty||function(t,e,r){t[e]=r.value},o="function"==typeof Symbol?Symbol:{},i=o.iterator||"@@iterator",a=o.asyncIterator||"@@asyncIterator",u=o.toStringTag||"@@toStringTag";function c(t,e,r){return Object.defineProperty(t,e,{value:r,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{c({},"")}catch(t){c=function(t,e,r){return t[e]=r}}function s(t,e,r,o){var i=e&&e.prototype instanceof h?e:h,a=Object.create(i.prototype),u=new S(o||[]);return n(a,"_invoke",{value:E(t,r,u)}),a}function l(t,e,r){try{return{type:"normal",arg:t.call(e,r)}}catch(t){return{type:"throw",arg:t}}}t.wrap=s;var f={};function h(){}function p(){}function d(){}var v={};c(v,i,(function(){return this}));var y=Object.getPrototypeOf,g=y&&y(y(j([])));g&&g!==e&&r.call(g,i)&&(v=g);var b=d.prototype=h.prototype=Object.create(v);function x(t){["next","throw","return"].forEach((function(e){c(t,e,(function(t){return this._invoke(e,t)}))}))}function L(t,e){function o(n,i,a,u){var c=l(t[n],t,i);if("throw"!==c.type){var s=c.arg,f=s.value;return f&&"object"==m(f)&&r.call(f,"__await")?e.resolve(f.__await).then((function(t){o("next",t,a,u)}),(function(t){o("throw",t,a,u)})):e.resolve(f).then((function(t){s.value=t,a(s)}),(function(t){return o("throw",t,a,u)}))}u(c.arg)}var i;n(this,"_invoke",{value:function(t,r){function n(){return new e((function(e,n){o(t,r,e,n)}))}return i=i?i.then(n,n):n()}})}function E(t,e,r){var n="suspendedStart";return function(o,i){if("executing"===n)throw new Error("Generator is already running");if("completed"===n){if("throw"===o)throw i;return P()}for(r.method=o,r.arg=i;;){var a=r.delegate;if(a){var u=k(a,r);if(u){if(u===f)continue;return u}}if("next"===r.method)r.sent=r._sent=r.arg;else if("throw"===r.method){if("suspendedStart"===n)throw n="completed",r.arg;r.dispatchException(r.arg)}else"return"===r.method&&r.abrupt("return",r.arg);n="executing";var c=l(t,e,r);if("normal"===c.type){if(n=r.done?"completed":"suspendedYield",c.arg===f)continue;return{value:c.arg,done:r.done}}"throw"===c.type&&(n="completed",r.method="throw",r.arg=c.arg)}}}function k(t,e){var r=e.method,n=t.iterator[r];if(void 0===n)return e.delegate=null,"throw"===r&&t.iterator.return&&(e.method="return",e.arg=void 0,k(t,e),"throw"===e.method)||"return"!==r&&(e.method="throw",e.arg=new TypeError("The iterator does not provide a '"+r+"' method")),f;var o=l(n,t.iterator,e.arg);if("throw"===o.type)return e.method="throw",e.arg=o.arg,e.delegate=null,f;var i=o.arg;return i?i.done?(e[t.resultName]=i.value,e.next=t.nextLoc,"return"!==e.method&&(e.method="next",e.arg=void 0),e.delegate=null,f):i:(e.method="throw",e.arg=new TypeError("iterator result is not an object"),e.delegate=null,f)}function _(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function O(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function S(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(_,this),this.reset(!0)}function j(t){if(t){var e=t[i];if(e)return e.call(t);if("function"==typeof t.next)return t;if(!isNaN(t.length)){var n=-1,o=function e(){for(;++n<t.length;)if(r.call(t,n))return e.value=t[n],e.done=!1,e;return e.value=void 0,e.done=!0,e};return o.next=o}}return{next:P}}function P(){return{value:void 0,done:!0}}return p.prototype=d,n(b,"constructor",{value:d,configurable:!0}),n(d,"constructor",{value:p,configurable:!0}),p.displayName=c(d,u,"GeneratorFunction"),t.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===p||"GeneratorFunction"===(e.displayName||e.name))},t.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,d):(t.__proto__=d,c(t,u,"GeneratorFunction")),t.prototype=Object.create(b),t},t.awrap=function(t){return{__await:t}},x(L.prototype),c(L.prototype,a,(function(){return this})),t.AsyncIterator=L,t.async=function(e,r,n,o,i){void 0===i&&(i=Promise);var a=new L(s(e,r,n,o),i);return t.isGeneratorFunction(r)?a:a.next().then((function(t){return t.done?t.value:a.next()}))},x(b),c(b,u,"Generator"),c(b,i,(function(){return this})),c(b,"toString",(function(){return"[object Generator]"})),t.keys=function(t){var e=Object(t),r=[];for(var n in e)r.push(n);return r.reverse(),function t(){for(;r.length;){var n=r.pop();if(n in e)return t.value=n,t.done=!1,t}return t.done=!0,t}},t.values=j,S.prototype={constructor:S,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=void 0,this.done=!1,this.delegate=null,this.method="next",this.arg=void 0,this.tryEntries.forEach(O),!t)for(var e in this)"t"===e.charAt(0)&&r.call(this,e)&&!isNaN(+e.slice(1))&&(this[e]=void 0)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var e=this;function n(r,n){return a.type="throw",a.arg=t,e.next=r,n&&(e.method="next",e.arg=void 0),!!n}for(var o=this.tryEntries.length-1;o>=0;--o){var i=this.tryEntries[o],a=i.completion;if("root"===i.tryLoc)return n("end");if(i.tryLoc<=this.prev){var u=r.call(i,"catchLoc"),c=r.call(i,"finallyLoc");if(u&&c){if(this.prev<i.catchLoc)return n(i.catchLoc,!0);if(this.prev<i.finallyLoc)return n(i.finallyLoc)}else if(u){if(this.prev<i.catchLoc)return n(i.catchLoc,!0)}else{if(!c)throw new Error("try statement without catch or finally");if(this.prev<i.finallyLoc)return n(i.finallyLoc)}}}},abrupt:function(t,e){for(var n=this.tryEntries.length-1;n>=0;--n){var o=this.tryEntries[n];if(o.tryLoc<=this.prev&&r.call(o,"finallyLoc")&&this.prev<o.finallyLoc){var i=o;break}}i&&("break"===t||"continue"===t)&&i.tryLoc<=e&&e<=i.finallyLoc&&(i=null);var a=i?i.completion:{};return a.type=t,a.arg=e,i?(this.method="next",this.next=i.finallyLoc,f):this.complete(a)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),f},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.finallyLoc===t)return this.complete(r.completion,r.afterLoc),O(r),f}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.tryLoc===t){var n=r.completion;if("throw"===n.type){var o=n.arg;O(r)}return o}}throw new Error("illegal catch attempt")},delegateYield:function(t,e,r){return this.delegate={iterator:j(t),resultName:e,nextLoc:r},"next"===this.method&&(this.arg=void 0),f}},t}function b(t,e,r,n,o,i,a){try{var u=t[i](a),c=u.value}catch(t){return void r(t)}u.done?e(c):Promise.resolve(c).then(n,o)}function x(t){return function(){var e=this,r=arguments;return new Promise((function(n,o){var i=t.apply(e,r);function a(t){b(i,n,o,a,u,"next",t)}function u(t){b(i,n,o,a,u,"throw",t)}a(void 0)}))}}var L=function(){var t=x(w().mark((function t(e,r,n,o){return w().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.abrupt("return",(0,a.AO)("POST",I.register_url,{email:e,username:r,password:n},o));case 1:case"end":return t.stop()}}),t)})));return function(e,r,n,o){return t.apply(this,arguments)}}(),E=function(){var t=x(w().mark((function t(e){return w().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.abrupt("return",(0,a.AO)("POST",I.verify_token_url,{},{Authorization:e}));case 1:case"end":return t.stop()}}),t)})));return function(e){return t.apply(this,arguments)}}();function k(t){return k="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},k(t)}function _(){_=function(){return t};var t={},e=Object.prototype,r=e.hasOwnProperty,n=Object.defineProperty||function(t,e,r){t[e]=r.value},o="function"==typeof Symbol?Symbol:{},i=o.iterator||"@@iterator",a=o.asyncIterator||"@@asyncIterator",u=o.toStringTag||"@@toStringTag";function c(t,e,r){return Object.defineProperty(t,e,{value:r,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{c({},"")}catch(t){c=function(t,e,r){return t[e]=r}}function s(t,e,r,o){var i=e&&e.prototype instanceof h?e:h,a=Object.create(i.prototype),u=new S(o||[]);return n(a,"_invoke",{value:x(t,r,u)}),a}function l(t,e,r){try{return{type:"normal",arg:t.call(e,r)}}catch(t){return{type:"throw",arg:t}}}t.wrap=s;var f={};function h(){}function p(){}function d(){}var v={};c(v,i,(function(){return this}));var y=Object.getPrototypeOf,g=y&&y(y(j([])));g&&g!==e&&r.call(g,i)&&(v=g);var m=d.prototype=h.prototype=Object.create(v);function w(t){["next","throw","return"].forEach((function(e){c(t,e,(function(t){return this._invoke(e,t)}))}))}function b(t,e){function o(n,i,a,u){var c=l(t[n],t,i);if("throw"!==c.type){var s=c.arg,f=s.value;return f&&"object"==k(f)&&r.call(f,"__await")?e.resolve(f.__await).then((function(t){o("next",t,a,u)}),(function(t){o("throw",t,a,u)})):e.resolve(f).then((function(t){s.value=t,a(s)}),(function(t){return o("throw",t,a,u)}))}u(c.arg)}var i;n(this,"_invoke",{value:function(t,r){function n(){return new e((function(e,n){o(t,r,e,n)}))}return i=i?i.then(n,n):n()}})}function x(t,e,r){var n="suspendedStart";return function(o,i){if("executing"===n)throw new Error("Generator is already running");if("completed"===n){if("throw"===o)throw i;return P()}for(r.method=o,r.arg=i;;){var a=r.delegate;if(a){var u=L(a,r);if(u){if(u===f)continue;return u}}if("next"===r.method)r.sent=r._sent=r.arg;else if("throw"===r.method){if("suspendedStart"===n)throw n="completed",r.arg;r.dispatchException(r.arg)}else"return"===r.method&&r.abrupt("return",r.arg);n="executing";var c=l(t,e,r);if("normal"===c.type){if(n=r.done?"completed":"suspendedYield",c.arg===f)continue;return{value:c.arg,done:r.done}}"throw"===c.type&&(n="completed",r.method="throw",r.arg=c.arg)}}}function L(t,e){var r=e.method,n=t.iterator[r];if(void 0===n)return e.delegate=null,"throw"===r&&t.iterator.return&&(e.method="return",e.arg=void 0,L(t,e),"throw"===e.method)||"return"!==r&&(e.method="throw",e.arg=new TypeError("The iterator does not provide a '"+r+"' method")),f;var o=l(n,t.iterator,e.arg);if("throw"===o.type)return e.method="throw",e.arg=o.arg,e.delegate=null,f;var i=o.arg;return i?i.done?(e[t.resultName]=i.value,e.next=t.nextLoc,"return"!==e.method&&(e.method="next",e.arg=void 0),e.delegate=null,f):i:(e.method="throw",e.arg=new TypeError("iterator result is not an object"),e.delegate=null,f)}function E(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function O(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function S(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(E,this),this.reset(!0)}function j(t){if(t){var e=t[i];if(e)return e.call(t);if("function"==typeof t.next)return t;if(!isNaN(t.length)){var n=-1,o=function e(){for(;++n<t.length;)if(r.call(t,n))return e.value=t[n],e.done=!1,e;return e.value=void 0,e.done=!0,e};return o.next=o}}return{next:P}}function P(){return{value:void 0,done:!0}}return p.prototype=d,n(m,"constructor",{value:d,configurable:!0}),n(d,"constructor",{value:p,configurable:!0}),p.displayName=c(d,u,"GeneratorFunction"),t.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===p||"GeneratorFunction"===(e.displayName||e.name))},t.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,d):(t.__proto__=d,c(t,u,"GeneratorFunction")),t.prototype=Object.create(m),t},t.awrap=function(t){return{__await:t}},w(b.prototype),c(b.prototype,a,(function(){return this})),t.AsyncIterator=b,t.async=function(e,r,n,o,i){void 0===i&&(i=Promise);var a=new b(s(e,r,n,o),i);return t.isGeneratorFunction(r)?a:a.next().then((function(t){return t.done?t.value:a.next()}))},w(m),c(m,u,"Generator"),c(m,i,(function(){return this})),c(m,"toString",(function(){return"[object Generator]"})),t.keys=function(t){var e=Object(t),r=[];for(var n in e)r.push(n);return r.reverse(),function t(){for(;r.length;){var n=r.pop();if(n in e)return t.value=n,t.done=!1,t}return t.done=!0,t}},t.values=j,S.prototype={constructor:S,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=void 0,this.done=!1,this.delegate=null,this.method="next",this.arg=void 0,this.tryEntries.forEach(O),!t)for(var e in this)"t"===e.charAt(0)&&r.call(this,e)&&!isNaN(+e.slice(1))&&(this[e]=void 0)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var e=this;function n(r,n){return a.type="throw",a.arg=t,e.next=r,n&&(e.method="next",e.arg=void 0),!!n}for(var o=this.tryEntries.length-1;o>=0;--o){var i=this.tryEntries[o],a=i.completion;if("root"===i.tryLoc)return n("end");if(i.tryLoc<=this.prev){var u=r.call(i,"catchLoc"),c=r.call(i,"finallyLoc");if(u&&c){if(this.prev<i.catchLoc)return n(i.catchLoc,!0);if(this.prev<i.finallyLoc)return n(i.finallyLoc)}else if(u){if(this.prev<i.catchLoc)return n(i.catchLoc,!0)}else{if(!c)throw new Error("try statement without catch or finally");if(this.prev<i.finallyLoc)return n(i.finallyLoc)}}}},abrupt:function(t,e){for(var n=this.tryEntries.length-1;n>=0;--n){var o=this.tryEntries[n];if(o.tryLoc<=this.prev&&r.call(o,"finallyLoc")&&this.prev<o.finallyLoc){var i=o;break}}i&&("break"===t||"continue"===t)&&i.tryLoc<=e&&e<=i.finallyLoc&&(i=null);var a=i?i.completion:{};return a.type=t,a.arg=e,i?(this.method="next",this.next=i.finallyLoc,f):this.complete(a)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),f},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.finallyLoc===t)return this.complete(r.completion,r.afterLoc),O(r),f}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.tryLoc===t){var n=r.completion;if("throw"===n.type){var o=n.arg;O(r)}return o}}throw new Error("illegal catch attempt")},delegateYield:function(t,e,r){return this.delegate={iterator:j(t),resultName:e,nextLoc:r},"next"===this.method&&(this.arg=void 0),f}},t}function O(t,e,r,n,o,i,a){try{var u=t[i](a),c=u.value}catch(t){return void r(t)}u.done?e(c):Promise.resolve(c).then(n,o)}function S(t){return function(){var e=this,r=arguments;return new Promise((function(n,o){var i=t.apply(e,r);function a(t){O(i,n,o,a,u,"next",t)}function u(t){O(i,n,o,a,u,"throw",t)}a(void 0)}))}}function j(t,e,r){return P.apply(this,arguments)}function P(){return(P=S(_().mark((function t(e,r,n){var o,i,a;return _().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(o=new URL(window.location.href),i=o.searchParams.get("instructions")){t.next=4;break}return t.abrupt("return");case 4:if(!0!==(a=JSON.parse(atob(i))).instructions.has_account){t.next=7;break}return t.abrupt("return",T(e,a.token));case 7:return a.instructions.needs_email||(r.parentElement.style.display="none"),n.value=a.user.given_name,r.value=a.user.email,t.abrupt("return",a.token);case 11:case"end":return t.stop()}}),t)})))).apply(this,arguments)}function A(){return(A=S(_().mark((function t(){var e,r,n,o,i,a,u;return _().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return e=document.querySelector('input[name="email"]'),r=document.querySelector('input[name="username"]'),n=document.querySelector('input[name="password"]'),o=document.querySelector('input[name="rp-password"]'),i=document.querySelector("#register-btn"),y(r),v(n),g(n,o),t.next=6,j(i,e,r);case 6:a=t.sent,u=function(){""===e.value.trim()||""===r.value.trim()||""===n.value.trim()||""===o.value.trim()?i.disabled=!0:i.disabled=!1},e.addEventListener("input",(function(){return u()})),r.addEventListener("input",(function(){return u()})),n.addEventListener("input",(function(){return u()})),o.addEventListener("input",(function(){return u()})),u(),i.addEventListener("click",(function(){return N(i,r,e,n,o,a)}));case 14:case"end":return t.stop()}}),t)})))).apply(this,arguments)}function N(t,e,r,n,o,i){return G.apply(this,arguments)}function G(){return(G=S(_().mark((function t(e,r,n,o,a,u){var c,s,l,h,v,y,g,m;return _().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(c=(0,i.ub)(e),s=d(r.value),l=p(o.value),o.value===a.value){t.next=8;break}return(0,i.Xj)("error","Passwords","Oops! It looks like your passwords don't match."),t.next=7,c();case 7:return t.abrupt("return",t.sent);case 8:if(!(s.length>0)){t.next=13;break}return(0,i.Xj)("error","Name","Oops! It looks like your name is invalid."),t.next=12,c();case 12:return t.abrupt("return",t.sent);case 13:if(!(l.length>0)){t.next=18;break}return(0,i.Xj)("error","Password","Oops! It looks like your password is invalid."),t.next=17,c();case 17:return t.abrupt("return",t.sent);case 18:if(0!==n.value.length){t.next=23;break}return(0,i.Xj)("error","Email","Oops! It looks like your email is invalid."),t.next=22,c();case 22:return t.abrupt("return",t.sent);case 23:return t.next=25,L(n.value,r.value,o.value,{Authorization:u});case 25:if(200===(h=t.sent).code||201===h.code){t.next=31;break}return(0,i.Xj)("error","Error",h.message),t.next=30,c();case 30:return t.abrupt("return",t.sent);case 31:if("verified"!==(v=h.data).type){t.next=38;break}return(0,i.Xj)("success","Success","Your account has been created successfully!"),t.next=36,T(e,v.token);case 36:t.next=42;break;case 38:y=v,g=document.querySelector("#resend-email"),m=document.querySelector("#resend"),g.value=n.value,Y("email_wait"),f(m,y.verify_token,y.resend_token,(function(){return g.value}));case 42:case"end":return t.stop()}}),t)})))).apply(this,arguments)}function T(t,e){return F.apply(this,arguments)}function F(){return(F=S(_().mark((function t(e,r){var n,o;return _().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return n=(0,i.ub)(e),t.next=3,E(r);case 3:if(200===(o=t.sent).code){t.next=7;break}return(0,i.Xj)("error","login",o.message),t.abrupt("return",n());case 7:return(0,i.Xj)("success","login","You have successfully logged in, redirecting you to the dashboard"),t.next=10,new Promise((function(){return setTimeout((function(){window.location.href="/"}),3e3)}));case 10:case"end":return t.stop()}}),t)})))).apply(this,arguments)}(0,n.Z)("register");var I=(0,o.MT)({verify_token_url:new o.Dy("data-token-url","string"),get_token_url:new o.Dy("data-get-token-url","string"),register_url:new o.Dy("data-register-url","string"),login_url:new o.Dy("data-login-url","string"),csrf_token:new o.Dy("data-csrf-token","string"),email_verify:new o.Dy("data-email-verify","string")}),q={register:document.querySelector('[data-panel-type="register"]'),email_wait:document.querySelector('[data-panel-type="email-wait"]')},X="register";function Y(t){var e=q[X];e.classList.add("login-area-panel-out"),e.classList.remove("login-area-panel-in");var r=q[t];r.style.opacity="1",r.classList.add("login-area-panel-in")}"true"!==q.register.getAttribute("data-in-progress")&&(q.register.setAttribute("data-in-progress","true"),function(){A.apply(this,arguments)}())}},t=>{t.O(0,[407,724,796,577],(()=>{return e=881,t(t.s=e);var e}));t.O()}]);