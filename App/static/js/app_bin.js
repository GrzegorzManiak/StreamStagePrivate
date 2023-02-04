(()=>{var e={903:(e,t,n)=>{var r,o;void 0===(o="function"==typeof(r=function(){"use strict";const t=[{id:0,value:"Too weak",minDiversity:0,minLength:0},{id:1,value:"Weak",minDiversity:2,minLength:6},{id:2,value:"Medium",minDiversity:4,minLength:8},{id:3,value:"Strong",minDiversity:4,minLength:10}];e.exports={passwordStrength:(e,n=t,r="!\"#$%&'()*+,-./:;<=>?@[\\\\\\]^_`{|}~")=>{let o=e||"";n[0].minDiversity=0,n[0].minLength=0;const a=[{regex:"[a-z]",message:"lowercase"},{regex:"[A-Z]",message:"uppercase"},{regex:"[0-9]",message:"number"}];r&&a.push({regex:`[${r}]`,message:"symbol"});let i={};i.contains=a.filter((e=>new RegExp(`${e.regex}`).test(o))).map((e=>e.message)),i.length=o.length;let s=n.filter((e=>i.contains.length>=e.minDiversity)).filter((e=>i.length>=e.minLength)).sort(((e,t)=>t.id-e.id)).map((e=>({id:e.id,value:e.value})));return Object.assign(i,s[0]),i},defaultOptions:t}})?r.call(t,n,t,e):r)||(e.exports=o)},313:(e,t)=>{"use strict";var n;function r(){["csrf_token","oauth_error","instructions","code"].forEach((function(e){document.cookie="".concat(e,"=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;")}))}function o(){var e=document.cookie.split(";"),t={};return e.forEach((function(e){var n=e.split("="),r=n[0],o=n[1];r=r.trim(),o=o.trim(),t[r]=o})),{csrf_token:t.csrftoken,oauth_error:t.oauth_error||null}}Object.defineProperty(t,"__esModule",{value:!0}),t.ensure_tokens=t.oauth_error=t.csrf_token=t.parse_cookies=t.delete_cookies=void 0,t.delete_cookies=r,t.parse_cookies=o,t.csrf_token=(n=o()).csrf_token,t.oauth_error=n.oauth_error,t.ensure_tokens=function(){t.csrf_token||(console.error("No CSRF token found"),r(),window.location.reload())}},187:(e,t,n)=>{"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.instruction_handler=void 0;var r=n(587),o=n(725);t.instruction_handler=function(e){var t=function(e){try{return JSON.parse(atob(e))}catch(e){return null}}(e);if(t)if("Success"===t.message){(0,r.hide_panel)("defualt"),(0,r.show_panel)("oauth");var n=(0,r.get_panel)("oauth"),a=n.element.querySelector('input[name="email"]');a.value=t.user.email,t.user.verified_email&&(a.parentElement.style.display="none"),n.element.querySelector('input[name="username"]').value=t.user.name;var i=n.element.querySelector('input[name="password"]');(0,o.attach_to_input)(i),n.element.querySelector('input[name="rp-password"]'),n.element.querySelector('button[type="submit"]')}else console.error(t.message)}},587:(e,t)=>{"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.hide_panel=t.show_panel=t.get_panel=t.panels=void 0;var n=Array.from(document.getElementsByClassName("panel"));t.panels=[],n.forEach((function(e){var n=e.getAttribute("data-panel-type");t.panels.push({type:n,element:e})})),t.get_panel=function(e){var n=t.panels.find((function(t){return t.type===e}));if(!n)throw new Error("No panel of type ".concat(e," found"));return n},t.show_panel=function(e){(0,t.get_panel)(e).element.style.display="block"},t.hide_panel=function(e){(0,t.get_panel)(e).element.style.display="none"}},725:(e,t,n)=>{"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.attach_to_input=void 0;var r=n(903);t.attach_to_input=function(e){var t="0";e.addEventListener("keyup",(function(){var n=(0,r.passwordStrength)(e.value);t=n.id.toString(),e.setAttribute("data-strength",t)})),e.addEventListener("blur",(function(){e.removeAttribute("data-strength")})),e.addEventListener("focus",(function(){e.setAttribute("data-strength",t)}))}},835:(e,t,n)=>{"use strict";t.ad=t.Is=void 0;var r=n(313),o=n(187);(0,r.ensure_tokens)();var a=new URL(window.location.href),i=a.searchParams.get("instructions"),s=a.searchParams.get("auth_token"),u=a.searchParams.get("code"),l=0,c=function(e){e&&l++};c(i),c(s),c(u),l>1&&window.location.reload();var d=document.getElementById("sso");t.Is=null==d?void 0:d.getAttribute("data-token-url"),t.ad=null==d?void 0:d.getAttribute("data-get-token-url"),t.Is&&t.ad||console.error("No token url or get token url or auth token"),i&&(0,o.instruction_handler)(i)}},t={};!function n(r){var o=t[r];if(void 0!==o)return o.exports;var a=t[r]={exports:{}};return e[r](a,a.exports,n),a.exports}(835)})();