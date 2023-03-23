/*! For license information please see homepage_bin.js.LICENSE.txt */
(()=>{"use strict";function t(e){return t="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},t(e)}function e(){e=function(){return r};var r={},n=Object.prototype,i=n.hasOwnProperty,o=Object.defineProperty||function(t,e,r){t[e]=r.value},a="function"==typeof Symbol?Symbol:{},c=a.iterator||"@@iterator",s=a.asyncIterator||"@@asyncIterator",l=a.toStringTag||"@@toStringTag";function u(t,e,r){return Object.defineProperty(t,e,{value:r,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{u({},"")}catch(t){u=function(t,e,r){return t[e]=r}}function f(t,e,r,n){var i=e&&e.prototype instanceof v?e:v,a=Object.create(i.prototype),c=new A(n||[]);return o(a,"_invoke",{value:x(t,r,c)}),a}function h(t,e,r){try{return{type:"normal",arg:t.call(e,r)}}catch(t){return{type:"throw",arg:t}}}r.wrap=f;var d={};function v(){}function p(){}function m(){}var y={};u(y,c,(function(){return this}));var g=Object.getPrototypeOf,w=g&&g(g(O([])));w&&w!==n&&i.call(w,c)&&(y=w);var b=m.prototype=v.prototype=Object.create(y);function _(t){["next","throw","return"].forEach((function(e){u(t,e,(function(t){return this._invoke(e,t)}))}))}function L(e,r){function n(o,a,c,s){var l=h(e[o],e,a);if("throw"!==l.type){var u=l.arg,f=u.value;return f&&"object"==t(f)&&i.call(f,"__await")?r.resolve(f.__await).then((function(t){n("next",t,c,s)}),(function(t){n("throw",t,c,s)})):r.resolve(f).then((function(t){u.value=t,c(u)}),(function(t){return n("throw",t,c,s)}))}s(l.arg)}var a;o(this,"_invoke",{value:function(t,e){function i(){return new r((function(r,i){n(t,e,r,i)}))}return a=a?a.then(i,i):i()}})}function x(t,e,r){var n="suspendedStart";return function(i,o){if("executing"===n)throw new Error("Generator is already running");if("completed"===n){if("throw"===i)throw o;return j()}for(r.method=i,r.arg=o;;){var a=r.delegate;if(a){var c=T(a,r);if(c){if(c===d)continue;return c}}if("next"===r.method)r.sent=r._sent=r.arg;else if("throw"===r.method){if("suspendedStart"===n)throw n="completed",r.arg;r.dispatchException(r.arg)}else"return"===r.method&&r.abrupt("return",r.arg);n="executing";var s=h(t,e,r);if("normal"===s.type){if(n=r.done?"completed":"suspendedYield",s.arg===d)continue;return{value:s.arg,done:r.done}}"throw"===s.type&&(n="completed",r.method="throw",r.arg=s.arg)}}}function T(t,e){var r=e.method,n=t.iterator[r];if(void 0===n)return e.delegate=null,"throw"===r&&t.iterator.return&&(e.method="return",e.arg=void 0,T(t,e),"throw"===e.method)||"return"!==r&&(e.method="throw",e.arg=new TypeError("The iterator does not provide a '"+r+"' method")),d;var i=h(n,t.iterator,e.arg);if("throw"===i.type)return e.method="throw",e.arg=i.arg,e.delegate=null,d;var o=i.arg;return o?o.done?(e[t.resultName]=o.value,e.next=t.nextLoc,"return"!==e.method&&(e.method="next",e.arg=void 0),e.delegate=null,d):o:(e.method="throw",e.arg=new TypeError("iterator result is not an object"),e.delegate=null,d)}function E(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function S(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function A(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(E,this),this.reset(!0)}function O(t){if(t){var e=t[c];if(e)return e.call(t);if("function"==typeof t.next)return t;if(!isNaN(t.length)){var r=-1,n=function e(){for(;++r<t.length;)if(i.call(t,r))return e.value=t[r],e.done=!1,e;return e.value=void 0,e.done=!0,e};return n.next=n}}return{next:j}}function j(){return{value:void 0,done:!0}}return p.prototype=m,o(b,"constructor",{value:m,configurable:!0}),o(m,"constructor",{value:p,configurable:!0}),p.displayName=u(m,l,"GeneratorFunction"),r.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===p||"GeneratorFunction"===(e.displayName||e.name))},r.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,m):(t.__proto__=m,u(t,l,"GeneratorFunction")),t.prototype=Object.create(b),t},r.awrap=function(t){return{__await:t}},_(L.prototype),u(L.prototype,s,(function(){return this})),r.AsyncIterator=L,r.async=function(t,e,n,i,o){void 0===o&&(o=Promise);var a=new L(f(t,e,n,i),o);return r.isGeneratorFunction(e)?a:a.next().then((function(t){return t.done?t.value:a.next()}))},_(b),u(b,l,"Generator"),u(b,c,(function(){return this})),u(b,"toString",(function(){return"[object Generator]"})),r.keys=function(t){var e=Object(t),r=[];for(var n in e)r.push(n);return r.reverse(),function t(){for(;r.length;){var n=r.pop();if(n in e)return t.value=n,t.done=!1,t}return t.done=!0,t}},r.values=O,A.prototype={constructor:A,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=void 0,this.done=!1,this.delegate=null,this.method="next",this.arg=void 0,this.tryEntries.forEach(S),!t)for(var e in this)"t"===e.charAt(0)&&i.call(this,e)&&!isNaN(+e.slice(1))&&(this[e]=void 0)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var e=this;function r(r,n){return a.type="throw",a.arg=t,e.next=r,n&&(e.method="next",e.arg=void 0),!!n}for(var n=this.tryEntries.length-1;n>=0;--n){var o=this.tryEntries[n],a=o.completion;if("root"===o.tryLoc)return r("end");if(o.tryLoc<=this.prev){var c=i.call(o,"catchLoc"),s=i.call(o,"finallyLoc");if(c&&s){if(this.prev<o.catchLoc)return r(o.catchLoc,!0);if(this.prev<o.finallyLoc)return r(o.finallyLoc)}else if(c){if(this.prev<o.catchLoc)return r(o.catchLoc,!0)}else{if(!s)throw new Error("try statement without catch or finally");if(this.prev<o.finallyLoc)return r(o.finallyLoc)}}}},abrupt:function(t,e){for(var r=this.tryEntries.length-1;r>=0;--r){var n=this.tryEntries[r];if(n.tryLoc<=this.prev&&i.call(n,"finallyLoc")&&this.prev<n.finallyLoc){var o=n;break}}o&&("break"===t||"continue"===t)&&o.tryLoc<=e&&e<=o.finallyLoc&&(o=null);var a=o?o.completion:{};return a.type=t,a.arg=e,o?(this.method="next",this.next=o.finallyLoc,d):this.complete(a)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),d},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.finallyLoc===t)return this.complete(r.completion,r.afterLoc),S(r),d}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.tryLoc===t){var n=r.completion;if("throw"===n.type){var i=n.arg;S(r)}return i}}throw new Error("illegal catch attempt")},delegateYield:function(t,e,r){return this.delegate={iterator:O(t),resultName:e,nextLoc:r},"next"===this.method&&(this.arg=void 0),d}},r}function r(t,e,r,n,i,o,a){try{var c=t[o](a),s=c.value}catch(t){return void r(t)}c.done?e(s):Promise.resolve(s).then(n,i)}function n(t){return n="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},n(t)}function i(){i=function(){return t};var t={},e=Object.prototype,r=e.hasOwnProperty,o=Object.defineProperty||function(t,e,r){t[e]=r.value},a="function"==typeof Symbol?Symbol:{},c=a.iterator||"@@iterator",s=a.asyncIterator||"@@asyncIterator",l=a.toStringTag||"@@toStringTag";function u(t,e,r){return Object.defineProperty(t,e,{value:r,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{u({},"")}catch(t){u=function(t,e,r){return t[e]=r}}function f(t,e,r,n){var i=e&&e.prototype instanceof v?e:v,a=Object.create(i.prototype),c=new A(n||[]);return o(a,"_invoke",{value:x(t,r,c)}),a}function h(t,e,r){try{return{type:"normal",arg:t.call(e,r)}}catch(t){return{type:"throw",arg:t}}}t.wrap=f;var d={};function v(){}function p(){}function m(){}var y={};u(y,c,(function(){return this}));var g=Object.getPrototypeOf,w=g&&g(g(O([])));w&&w!==e&&r.call(w,c)&&(y=w);var b=m.prototype=v.prototype=Object.create(y);function _(t){["next","throw","return"].forEach((function(e){u(t,e,(function(t){return this._invoke(e,t)}))}))}function L(t,e){function i(o,a,c,s){var l=h(t[o],t,a);if("throw"!==l.type){var u=l.arg,f=u.value;return f&&"object"==n(f)&&r.call(f,"__await")?e.resolve(f.__await).then((function(t){i("next",t,c,s)}),(function(t){i("throw",t,c,s)})):e.resolve(f).then((function(t){u.value=t,c(u)}),(function(t){return i("throw",t,c,s)}))}s(l.arg)}var a;o(this,"_invoke",{value:function(t,r){function n(){return new e((function(e,n){i(t,r,e,n)}))}return a=a?a.then(n,n):n()}})}function x(t,e,r){var n="suspendedStart";return function(i,o){if("executing"===n)throw new Error("Generator is already running");if("completed"===n){if("throw"===i)throw o;return j()}for(r.method=i,r.arg=o;;){var a=r.delegate;if(a){var c=T(a,r);if(c){if(c===d)continue;return c}}if("next"===r.method)r.sent=r._sent=r.arg;else if("throw"===r.method){if("suspendedStart"===n)throw n="completed",r.arg;r.dispatchException(r.arg)}else"return"===r.method&&r.abrupt("return",r.arg);n="executing";var s=h(t,e,r);if("normal"===s.type){if(n=r.done?"completed":"suspendedYield",s.arg===d)continue;return{value:s.arg,done:r.done}}"throw"===s.type&&(n="completed",r.method="throw",r.arg=s.arg)}}}function T(t,e){var r=e.method,n=t.iterator[r];if(void 0===n)return e.delegate=null,"throw"===r&&t.iterator.return&&(e.method="return",e.arg=void 0,T(t,e),"throw"===e.method)||"return"!==r&&(e.method="throw",e.arg=new TypeError("The iterator does not provide a '"+r+"' method")),d;var i=h(n,t.iterator,e.arg);if("throw"===i.type)return e.method="throw",e.arg=i.arg,e.delegate=null,d;var o=i.arg;return o?o.done?(e[t.resultName]=o.value,e.next=t.nextLoc,"return"!==e.method&&(e.method="next",e.arg=void 0),e.delegate=null,d):o:(e.method="throw",e.arg=new TypeError("iterator result is not an object"),e.delegate=null,d)}function E(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function S(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function A(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(E,this),this.reset(!0)}function O(t){if(t){var e=t[c];if(e)return e.call(t);if("function"==typeof t.next)return t;if(!isNaN(t.length)){var n=-1,i=function e(){for(;++n<t.length;)if(r.call(t,n))return e.value=t[n],e.done=!1,e;return e.value=void 0,e.done=!0,e};return i.next=i}}return{next:j}}function j(){return{value:void 0,done:!0}}return p.prototype=m,o(b,"constructor",{value:m,configurable:!0}),o(m,"constructor",{value:p,configurable:!0}),p.displayName=u(m,l,"GeneratorFunction"),t.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===p||"GeneratorFunction"===(e.displayName||e.name))},t.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,m):(t.__proto__=m,u(t,l,"GeneratorFunction")),t.prototype=Object.create(b),t},t.awrap=function(t){return{__await:t}},_(L.prototype),u(L.prototype,s,(function(){return this})),t.AsyncIterator=L,t.async=function(e,r,n,i,o){void 0===o&&(o=Promise);var a=new L(f(e,r,n,i),o);return t.isGeneratorFunction(r)?a:a.next().then((function(t){return t.done?t.value:a.next()}))},_(b),u(b,l,"Generator"),u(b,c,(function(){return this})),u(b,"toString",(function(){return"[object Generator]"})),t.keys=function(t){var e=Object(t),r=[];for(var n in e)r.push(n);return r.reverse(),function t(){for(;r.length;){var n=r.pop();if(n in e)return t.value=n,t.done=!1,t}return t.done=!0,t}},t.values=O,A.prototype={constructor:A,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=void 0,this.done=!1,this.delegate=null,this.method="next",this.arg=void 0,this.tryEntries.forEach(S),!t)for(var e in this)"t"===e.charAt(0)&&r.call(this,e)&&!isNaN(+e.slice(1))&&(this[e]=void 0)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var e=this;function n(r,n){return a.type="throw",a.arg=t,e.next=r,n&&(e.method="next",e.arg=void 0),!!n}for(var i=this.tryEntries.length-1;i>=0;--i){var o=this.tryEntries[i],a=o.completion;if("root"===o.tryLoc)return n("end");if(o.tryLoc<=this.prev){var c=r.call(o,"catchLoc"),s=r.call(o,"finallyLoc");if(c&&s){if(this.prev<o.catchLoc)return n(o.catchLoc,!0);if(this.prev<o.finallyLoc)return n(o.finallyLoc)}else if(c){if(this.prev<o.catchLoc)return n(o.catchLoc,!0)}else{if(!s)throw new Error("try statement without catch or finally");if(this.prev<o.finallyLoc)return n(o.finallyLoc)}}}},abrupt:function(t,e){for(var n=this.tryEntries.length-1;n>=0;--n){var i=this.tryEntries[n];if(i.tryLoc<=this.prev&&r.call(i,"finallyLoc")&&this.prev<i.finallyLoc){var o=i;break}}o&&("break"===t||"continue"===t)&&o.tryLoc<=e&&e<=o.finallyLoc&&(o=null);var a=o?o.completion:{};return a.type=t,a.arg=e,o?(this.method="next",this.next=o.finallyLoc,d):this.complete(a)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),d},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.finallyLoc===t)return this.complete(r.completion,r.afterLoc),S(r),d}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.tryLoc===t){var n=r.completion;if("throw"===n.type){var i=n.arg;S(r)}return i}}throw new Error("illegal catch attempt")},delegateYield:function(t,e,r){return this.delegate={iterator:O(t),resultName:e,nextLoc:r},"next"===this.method&&(this.arg=void 0),d}},t}function o(t,e,r,n,i,o,a){try{var c=t[o](a),s=c.value}catch(t){return void r(t)}c.done?e(s):Promise.resolve(s).then(n,i)}function a(t){return function(){var e=this,r=arguments;return new Promise((function(n,i){var a=t.apply(e,r);function c(t){o(a,n,i,c,s,"next",t)}function s(t){o(a,n,i,c,s,"throw",t)}c(void 0)}))}}function c(){return c=a(i().mark((function t(e,r){var n,o,c,s,l,u=arguments;return i().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(n=u.length>2&&void 0!==u[2]?u[2]:500,o=document.querySelector(e),c=document.querySelector(r),o&&c){t.next=4;break}return t.abrupt("return");case 4:s=-1,l=function(){var t=a(i().mark((function t(){var e;return i().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:e=!0,o.classList.add("show"),c.classList.add("show");case 3:if(!e){t.next=10;break}return t.next=6,new Promise((function(t){return setTimeout(t,100)}));case 6:e=o.matches(":hover")||c.matches(":hover"),s=Date.now(),t.next=3;break;case 10:case"end":return t.stop()}}),t)})));return function(){return t.apply(this,arguments)}}(),o.addEventListener("mousemove",(function(){return l()})),c.addEventListener("mousemove",(function(){return l()})),setInterval((function(){s>Date.now()-n||(o.classList.remove("show"),c.classList.remove("show"))}));case 9:case"end":return t.stop()}}),t)}))),c.apply(this,arguments)}function s(t,e){var r="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(!r){if(Array.isArray(t)||(r=function(t,e){if(!t)return;if("string"==typeof t)return l(t,e);var r=Object.prototype.toString.call(t).slice(8,-1);"Object"===r&&t.constructor&&(r=t.constructor.name);if("Map"===r||"Set"===r)return Array.from(t);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return l(t,e)}(t))||e&&t&&"number"==typeof t.length){r&&(t=r);var n=0,i=function(){};return{s:i,n:function(){return n>=t.length?{done:!0}:{done:!1,value:t[n++]}},e:function(t){throw t},f:i}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var o,a=!0,c=!1;return{s:function(){r=r.call(t)},n:function(){var t=r.next();return a=t.done,t},e:function(t){c=!0,o=t},f:function(){try{a||null==r.return||r.return()}finally{if(c)throw o}}}}function l(t,e){(null==e||e>t.length)&&(e=t.length);for(var r=0,n=new Array(e);r<e;r++)n[r]=t[r];return n}var u=document.getElementById("thumbnail"),f=document.getElementById("carousel");function h(t){var e=u.cloneNode(!0);e.id="thumbnail-"+t.id,e.setAttribute("data-is-live",t.is_live.toString()),e.setAttribute("data-is-hidden","false"),e.setAttribute("data-is-skeleton","false");e.querySelector('[data-elm="main-image"]'),e.querySelector('[data-elm="pfp"]');var r=e.querySelector('[data-elm="title"]'),n=e.querySelector('[data-elm="view-count"]'),i=e.querySelector('[data-elm="date-vod"]');return r.innerText=t.title,n.innerText=t.views_formatted+" views",i.innerText=t.start_time,e}u.id="",f.id="";var d={id:"1",name:"Test Streamer",pfp:"https://via.placeholder.com/300x300"},v=[{id:"1",is_live:!1,title:"Test Title 1",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"2",is_live:!0,title:"Test Title 2",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"3",is_live:!0,title:"Test Title 3",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"4",is_live:!1,title:"Test Title 4",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"5",is_live:!1,title:"Test Title 5",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"6",is_live:!0,title:"Test Title 6",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"7",is_live:!1,title:"Test Title 7",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"8",is_live:!0,title:"Test Title 8",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"9",is_live:!1,title:"Test Title 9",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"10",is_live:!1,title:"Test Title 0",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"11",is_live:!0,title:"Test Title 11",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"12",is_live:!0,title:"Test Title 12",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"13",is_live:!1,title:"Test Title 13",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"14",is_live:!1,title:"Test Title 14",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d},{id:"15",is_live:!0,title:"Test Title 15",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:d}];!function(t,e){var r=function(t,e){var r=f.cloneNode(!0);r.id="carousel-"+e[0].id,t.appendChild(r),r.removeAttribute("data-is-hidden");var n,i=t.querySelector(".carousel-content"),o=s(e);try{for(o.s();!(n=o.n()).done;){var a=h(n.value);i.appendChild(a),a.setAttribute("tabindex",(0).toString())}}catch(t){o.e(t)}finally{o.f()}return{parent:i,children:Array.from(i.children)}}(t,e),n=r.parent,i=r.children,o=t.querySelector(".carousel-button-left"),a=t.querySelector(".carousel-button-right"),c=!1,l=!1,u=t.querySelector(".scroll-indicator"),d=function(){var t=n.scrollLeft,e=n.offsetWidth,r=i[0].clientWidth;t+e>=n.scrollWidth-r?(n.scrollLeft=0,l=!1,c=!0):t<=0&&(n.scrollLeft=n.scrollWidth-e,c=!1,l=!0)};o.addEventListener("click",(function(){var t=n.children[0].clientWidth;n.scrollLeft-=t,!1===c&&n.scrollLeft<=t?c=!0:c?(c=!1,d()):l=!1})),a.addEventListener("click",(function(){var t=n.children[0].clientWidth,e=n.offsetWidth;n.scrollLeft+=t,!1===l&&n.scrollLeft+e>=n.scrollWidth-t?l=!0:l?(l=!1,d()):c=!1})),n.scrollLeft=0,c=!0,l=!1,n.addEventListener("scroll",(function(){var t=n.scrollLeft,e=n.offsetWidth,r=t/(n.scrollWidth-e);u.style.width=100*r+"%"}))}(document.querySelector("#c1"),v);var p,m,y;document.querySelector("#logo-loader");p=document.getElementsByClassName("showcase"),Array.from(p).forEach((function(t){return function(t){var n=t.getElementsByClassName("showcase-small-img"),i=t.getElementsByClassName("showcase-big")[0];Array.from(n).forEach((function(t,o){return t.addEventListener("click",(function(){Array.from(n).forEach(function(){var t,n=(t=e().mark((function t(r){return e().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.abrupt("return",r.classList.remove("active"));case 1:case"end":return t.stop()}}),t)})),function(){var e=this,n=arguments;return new Promise((function(i,o){var a=t.apply(e,n);function c(t){r(a,i,o,c,s,"next",t)}function s(t){r(a,i,o,c,s,"throw",t)}c(void 0)}))});return function(t){return n.apply(this,arguments)}}()),t.classList.add("active"),i.style.backgroundImage="url("+t.getAttribute("data-stream-big")+")",i.querySelector('[data-sci-elm="title"]').innerHTML=t.getAttribute("data-stream-title");var o=i.querySelector('[data-sci-elm="desc"]');o.querySelector(".description").innerHTML=t.getAttribute("data-stream-desc"),o.querySelector('[data-skeleton="image"]').setAttribute("src",t.getAttribute("data-stream-pfp")),o.querySelector('[data-elm="view-count"]').innerHTML=t.getAttribute("data-stream-views"),o.querySelector('[data-elm="date-vod"]').innerHTML=t.getAttribute("data-stream-date"),o.setAttribute("data-is-live",t.getAttribute("data-is-live"));var a=t.getAttribute("data-stream-tags").split(","),c=i.querySelector(".tags");c.innerHTML="",a.forEach((function(t){var e=document.createElement("span");e.classList.add("tag"),e.setAttribute("data-tag","info"),"18+"===(t=t.trim())&&e.setAttribute("data-tag","error"),e.innerHTML=t,c.appendChild(e)}))}))})),n[1].click()}(t)})),m=document.getElementById("nav"),y=function(){window.scrollY>50?m.classList.add("scrolled"):m.classList.remove("scrolled")},window.addEventListener("scroll",(function(){return y()})),y(),function(t,e){c.apply(this,arguments)}("#nav .nav-dropdown-menu","#nav .nav-dropdown-toggle")})();