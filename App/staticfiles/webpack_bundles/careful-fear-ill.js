/*! For license information please see careful-fear-ill.js.LICENSE.txt */
"use strict";(self.webpackChunk=self.webpackChunk||[]).push([[796,335,440],{440:(t,r,e)=>{e.d(r,{AO:()=>m,gW:()=>x,s1:()=>w});var n=e(609),o=e(724);function i(t){return i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},i(t)}function a(t,r){var e=Object.keys(t);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(t);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(t,r).enumerable}))),e.push.apply(e,n)}return e}function c(t){for(var r=1;r<arguments.length;r++){var e=null!=arguments[r]?arguments[r]:{};r%2?a(Object(e),!0).forEach((function(r){u(t,r,e[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(e)):a(Object(e)).forEach((function(r){Object.defineProperty(t,r,Object.getOwnPropertyDescriptor(e,r))}))}return t}function u(t,r,e){return(r=function(t){var r=function(t,r){if("object"!==i(t)||null===t)return t;var e=t[Symbol.toPrimitive];if(void 0!==e){var n=e.call(t,r||"default");if("object"!==i(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===r?String:Number)(t)}(t,"string");return"symbol"===i(r)?r:String(r)}(r))in t?Object.defineProperty(t,r,{value:e,enumerable:!0,configurable:!0,writable:!0}):t[r]=e,t}function s(){s=function(){return t};var t={},r=Object.prototype,e=r.hasOwnProperty,n=Object.defineProperty||function(t,r,e){t[r]=e.value},o="function"==typeof Symbol?Symbol:{},a=o.iterator||"@@iterator",c=o.asyncIterator||"@@asyncIterator",u=o.toStringTag||"@@toStringTag";function f(t,r,e){return Object.defineProperty(t,r,{value:e,enumerable:!0,configurable:!0,writable:!0}),t[r]}try{f({},"")}catch(t){f=function(t,r,e){return t[r]=e}}function l(t,r,e,o){var i=r&&r.prototype instanceof v?r:v,a=Object.create(i.prototype),c=new S(o||[]);return n(a,"_invoke",{value:j(t,e,c)}),a}function h(t,r,e){try{return{type:"normal",arg:t.call(r,e)}}catch(t){return{type:"throw",arg:t}}}t.wrap=l;var p={};function v(){}function y(){}function d(){}var m={};f(m,a,(function(){return this}));var g=Object.getPrototypeOf,b=g&&g(g(P([])));b&&b!==r&&e.call(b,a)&&(m=b);var w=d.prototype=v.prototype=Object.create(m);function x(t){["next","throw","return"].forEach((function(r){f(t,r,(function(t){return this._invoke(r,t)}))}))}function O(t,r){function o(n,a,c,u){var s=h(t[n],t,a);if("throw"!==s.type){var f=s.arg,l=f.value;return l&&"object"==i(l)&&e.call(l,"__await")?r.resolve(l.__await).then((function(t){o("next",t,c,u)}),(function(t){o("throw",t,c,u)})):r.resolve(l).then((function(t){f.value=t,c(f)}),(function(t){return o("throw",t,c,u)}))}u(s.arg)}var a;n(this,"_invoke",{value:function(t,e){function n(){return new r((function(r,n){o(t,e,r,n)}))}return a=a?a.then(n,n):n()}})}function j(t,r,e){var n="suspendedStart";return function(o,i){if("executing"===n)throw new Error("Generator is already running");if("completed"===n){if("throw"===o)throw i;return _()}for(e.method=o,e.arg=i;;){var a=e.delegate;if(a){var c=k(a,e);if(c){if(c===p)continue;return c}}if("next"===e.method)e.sent=e._sent=e.arg;else if("throw"===e.method){if("suspendedStart"===n)throw n="completed",e.arg;e.dispatchException(e.arg)}else"return"===e.method&&e.abrupt("return",e.arg);n="executing";var u=h(t,r,e);if("normal"===u.type){if(n=e.done?"completed":"suspendedYield",u.arg===p)continue;return{value:u.arg,done:e.done}}"throw"===u.type&&(n="completed",e.method="throw",e.arg=u.arg)}}}function k(t,r){var e=r.method,n=t.iterator[e];if(void 0===n)return r.delegate=null,"throw"===e&&t.iterator.return&&(r.method="return",r.arg=void 0,k(t,r),"throw"===r.method)||"return"!==e&&(r.method="throw",r.arg=new TypeError("The iterator does not provide a '"+e+"' method")),p;var o=h(n,t.iterator,r.arg);if("throw"===o.type)return r.method="throw",r.arg=o.arg,r.delegate=null,p;var i=o.arg;return i?i.done?(r[t.resultName]=i.value,r.next=t.nextLoc,"return"!==r.method&&(r.method="next",r.arg=void 0),r.delegate=null,p):i:(r.method="throw",r.arg=new TypeError("iterator result is not an object"),r.delegate=null,p)}function E(t){var r={tryLoc:t[0]};1 in t&&(r.catchLoc=t[1]),2 in t&&(r.finallyLoc=t[2],r.afterLoc=t[3]),this.tryEntries.push(r)}function L(t){var r=t.completion||{};r.type="normal",delete r.arg,t.completion=r}function S(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(E,this),this.reset(!0)}function P(t){if(t){var r=t[a];if(r)return r.call(t);if("function"==typeof t.next)return t;if(!isNaN(t.length)){var n=-1,o=function r(){for(;++n<t.length;)if(e.call(t,n))return r.value=t[n],r.done=!1,r;return r.value=void 0,r.done=!0,r};return o.next=o}}return{next:_}}function _(){return{value:void 0,done:!0}}return y.prototype=d,n(w,"constructor",{value:d,configurable:!0}),n(d,"constructor",{value:y,configurable:!0}),y.displayName=f(d,u,"GeneratorFunction"),t.isGeneratorFunction=function(t){var r="function"==typeof t&&t.constructor;return!!r&&(r===y||"GeneratorFunction"===(r.displayName||r.name))},t.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,d):(t.__proto__=d,f(t,u,"GeneratorFunction")),t.prototype=Object.create(w),t},t.awrap=function(t){return{__await:t}},x(O.prototype),f(O.prototype,c,(function(){return this})),t.AsyncIterator=O,t.async=function(r,e,n,o,i){void 0===i&&(i=Promise);var a=new O(l(r,e,n,o),i);return t.isGeneratorFunction(e)?a:a.next().then((function(t){return t.done?t.value:a.next()}))},x(w),f(w,u,"Generator"),f(w,a,(function(){return this})),f(w,"toString",(function(){return"[object Generator]"})),t.keys=function(t){var r=Object(t),e=[];for(var n in r)e.push(n);return e.reverse(),function t(){for(;e.length;){var n=e.pop();if(n in r)return t.value=n,t.done=!1,t}return t.done=!0,t}},t.values=P,S.prototype={constructor:S,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=void 0,this.done=!1,this.delegate=null,this.method="next",this.arg=void 0,this.tryEntries.forEach(L),!t)for(var r in this)"t"===r.charAt(0)&&e.call(this,r)&&!isNaN(+r.slice(1))&&(this[r]=void 0)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var r=this;function n(e,n){return a.type="throw",a.arg=t,r.next=e,n&&(r.method="next",r.arg=void 0),!!n}for(var o=this.tryEntries.length-1;o>=0;--o){var i=this.tryEntries[o],a=i.completion;if("root"===i.tryLoc)return n("end");if(i.tryLoc<=this.prev){var c=e.call(i,"catchLoc"),u=e.call(i,"finallyLoc");if(c&&u){if(this.prev<i.catchLoc)return n(i.catchLoc,!0);if(this.prev<i.finallyLoc)return n(i.finallyLoc)}else if(c){if(this.prev<i.catchLoc)return n(i.catchLoc,!0)}else{if(!u)throw new Error("try statement without catch or finally");if(this.prev<i.finallyLoc)return n(i.finallyLoc)}}}},abrupt:function(t,r){for(var n=this.tryEntries.length-1;n>=0;--n){var o=this.tryEntries[n];if(o.tryLoc<=this.prev&&e.call(o,"finallyLoc")&&this.prev<o.finallyLoc){var i=o;break}}i&&("break"===t||"continue"===t)&&i.tryLoc<=r&&r<=i.finallyLoc&&(i=null);var a=i?i.completion:{};return a.type=t,a.arg=r,i?(this.method="next",this.next=i.finallyLoc,p):this.complete(a)},complete:function(t,r){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&r&&(this.next=r),p},finish:function(t){for(var r=this.tryEntries.length-1;r>=0;--r){var e=this.tryEntries[r];if(e.finallyLoc===t)return this.complete(e.completion,e.afterLoc),L(e),p}},catch:function(t){for(var r=this.tryEntries.length-1;r>=0;--r){var e=this.tryEntries[r];if(e.tryLoc===t){var n=e.completion;if("throw"===n.type){var o=n.arg;L(e)}return o}}throw new Error("illegal catch attempt")},delegateYield:function(t,r,e){return this.delegate={iterator:P(t),resultName:r,nextLoc:e},"next"===this.method&&(this.arg=void 0),p}},t}function f(t,r,e,n,o,i,a){try{var c=t[i](a),u=c.value}catch(t){return void e(t)}c.done?r(u):Promise.resolve(u).then(n,o)}function l(t){return function(){var r=this,e=arguments;return new Promise((function(n,o){var i=t.apply(r,e);function a(t){f(i,n,o,a,c,"next",t)}function c(t){f(i,n,o,a,c,"throw",t)}a(void 0)}))}}function h(t,r){var e="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(!e){if(Array.isArray(t)||(e=function(t,r){if(!t)return;if("string"==typeof t)return p(t,r);var e=Object.prototype.toString.call(t).slice(8,-1);"Object"===e&&t.constructor&&(e=t.constructor.name);if("Map"===e||"Set"===e)return Array.from(t);if("Arguments"===e||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(e))return p(t,r)}(t))||r&&t&&"number"==typeof t.length){e&&(t=e);var n=0,o=function(){};return{s:o,n:function(){return n>=t.length?{done:!0}:{done:!1,value:t[n++]}},e:function(t){throw t},f:o}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var i,a=!0,c=!1;return{s:function(){e=e.call(t)},n:function(){var t=e.next();return a=t.done,t},e:function(t){c=!0,i=t},f:function(){try{a||null==e.return||e.return()}finally{if(c)throw i}}}}function p(t,r){(null==r||r>t.length)&&(r=t.length);for(var e=0,n=new Array(r);e<r;e++)n[e]=t[e];return n}var v=new URL(window.location.href).searchParams.get("impersonate"),y="streamstage-token";function d(){var t,r=h(document.cookie.split(";"));try{for(r.s();!(t=r.n()).done;){var e=t.value;if(e.split("=")[0].trim()===y)return e.split("=")[1]}}catch(t){r.e(t)}finally{r.f()}}function m(t,r){return g.apply(this,arguments)}function g(){return g=l(s().mark((function t(r,e){var n,i,a,u,f,l,h,p,m,g,b=arguments;return s().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:for(l in n=b.length>2&&void 0!==b[2]?b[2]:{},i=b.length>3&&void 0!==b[3]?b[3]:{},a=d(),u="","GET"===r&&(u=Object.keys(n).map((function(t){return encodeURIComponent(t)+"="+encodeURIComponent(n[t])})).join("&")),f={},n)void 0!==n[l]&&null!==n[l]&&(f[l]=n[l]);for(p in i.Impersonate=v,i[y]=a,h={},i)void 0!==i[p]&&null!==i[p]&&(h[p]=i[p]);return t.next=13,fetch(e+("GET"===r?"?"+u:""),{method:r,headers:c({"Content-Type":"application/json","X-CSRFToken":(0,o.DN)().csrf_token,"ss-CSRF-token":(0,o.DN)().csrf_token},h),body:"GET"===r?void 0:JSON.stringify(f)});case 13:return m=t.sent,t.prev=14,t.next=17,m.json();case 17:return g=t.sent,t.abrupt("return",{data:g.data,code:m.status,message:g.message});case 21:return t.prev=21,t.t0=t.catch(14),t.abrupt("return",{code:m.status,message:"Oops! It appears that our servers dont want to talk to us right now. Please try again later."});case 24:case"end":return t.stop()}}),t,null,[[14,21]])}))),g.apply(this,arguments)}var b=function(){var t=l(s().mark((function t(r){return s().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.abrupt("return",m("POST",(0,o.DN)().recent_verification,{token:r}));case 1:case"end":return t.stop()}}),t)})));return function(r){return t.apply(this,arguments)}}(),w=function(){var t=l(s().mark((function t(r,e){return s().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.abrupt("return",m("POST",(0,o.DN)().resend_verification,{token:r,email:e}));case 1:case"end":return t.stop()}}),t)})));return function(r,e){return t.apply(this,arguments)}}();function x(t){return O.apply(this,arguments)}function O(){return O=l(s().mark((function t(r){var e,o,i,a=arguments;return s().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return e=a.length>1&&void 0!==a[1]?a[1]:3e3,o=a.length>2&&void 0!==a[2]?a[2]:9e5,i=a.length>3&&void 0!==a[3]?a[3]:"Your email has been verified, you'll be given access to your account in a few seconds.",t.abrupt("return",new Promise(function(){var t=l(s().mark((function t(a,c){var u,f;return s().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:u=!1,f=setInterval(l(s().mark((function t(){var e;return s().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,b(r());case 2:if(404!==(e=t.sent).code){t.next=6;break}t.next=16;break;case 6:if(200!==e.code){t.next=13;break}return(0,n.Xj)("success","Congratulations!",i),clearInterval(f),u=!0,t.abrupt("return",a(!0));case 13:return(0,n.Xj)("error","Error",e.message),clearInterval(f),t.abrupt("return",c(!1));case 16:case"end":return t.stop()}}),t)}))),e),setTimeout((function(){clearInterval(f),c(!1),u||(0,n.Xj)("error","Error","The verification email has expired")}),o);case 3:case"end":return t.stop()}}),t)})));return function(r,e){return t.apply(this,arguments)}}()));case 4:case"end":return t.stop()}}),t)}))),O.apply(this,arguments)}}}]);