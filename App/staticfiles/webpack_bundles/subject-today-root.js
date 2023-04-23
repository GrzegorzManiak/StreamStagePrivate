/*! For license information please see subject-today-root.js.LICENSE.txt */
"use strict";(self.webpackChunk=self.webpackChunk||[]).push([[772],{193:(e,t,f)=>{function r(e){return e+.5|0}f.d(t,{Il:()=>A});const a=(e,t,f)=>Math.max(Math.min(e,f),t);function n(e){return a(r(2.55*e),0,255)}function s(e){return a(r(255*e),0,255)}function i(e){return a(r(e/2.55)/100,0,1)}function c(e){return a(r(100*e),0,100)}const b={0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,A:10,B:11,C:12,D:13,E:14,F:15,a:10,b:11,c:12,d:13,e:14,f:15},g=[..."0123456789ABCDEF"],d=e=>g[15&e],o=e=>g[(240&e)>>4]+g[15&e],u=e=>(240&e)>>4==(15&e);function h(e){var t=(e=>u(e.r)&&u(e.g)&&u(e.b)&&u(e.a))(e)?d:o;return e?"#"+t(e.r)+t(e.g)+t(e.b)+((e,t)=>e<255?t(e):"")(e.a,t):void 0}const l=/^(hsla?|hwb|hsv)\(\s*([-+.e\d]+)(?:deg)?[\s,]+([-+.e\d]+)%[\s,]+([-+.e\d]+)%(?:[\s,]+([-+.e\d]+)(%)?)?\s*\)$/;function p(e,t,f){const r=t*Math.min(f,1-f),a=(t,a=(t+e/30)%12)=>f-r*Math.max(Math.min(a-3,9-a,1),-1);return[a(0),a(8),a(4)]}function m(e,t,f){const r=(r,a=(r+e/60)%6)=>f-f*t*Math.max(Math.min(a,4-a,1),0);return[r(5),r(3),r(1)]}function y(e,t,f){const r=p(e,1,.5);let a;for(t+f>1&&(a=1/(t+f),t*=a,f*=a),a=0;a<3;a++)r[a]*=1-t-f,r[a]+=t;return r}function Y(e){const t=e.r/255,f=e.g/255,r=e.b/255,a=Math.max(t,f,r),n=Math.min(t,f,r),s=(a+n)/2;let i,c,b;return a!==n&&(b=a-n,c=s>.5?b/(2-a-n):b/(a+n),i=function(e,t,f,r,a){return e===a?(t-f)/r+(t<f?6:0):t===a?(f-e)/r+2:(e-t)/r+4}(t,f,r,b,a),i=60*i+.5),[0|i,c||0,s]}function v(e,t,f,r){return(Array.isArray(t)?e(t[0],t[1],t[2]):e(t,f,r)).map(s)}function w(e,t,f){return v(p,e,t,f)}function x(e){return(e%360+360)%360}function k(e){const t=l.exec(e);let f,r=255;if(!t)return;t[5]!==f&&(r=t[6]?n(+t[5]):s(+t[5]));const a=x(+t[2]),i=+t[3]/100,c=+t[4]/100;return f="hwb"===t[1]?function(e,t,f){return v(y,e,t,f)}(a,i,c):"hsv"===t[1]?function(e,t,f){return v(m,e,t,f)}(a,i,c):w(a,i,c),{r:f[0],g:f[1],b:f[2],a:r}}const F={x:"dark",Z:"light",Y:"re",X:"blu",W:"gr",V:"medium",U:"slate",A:"ee",T:"ol",S:"or",B:"ra",C:"lateg",D:"ights",R:"in",Q:"turquois",E:"hi",P:"ro",O:"al",N:"le",M:"de",L:"yello",F:"en",K:"ch",G:"arks",H:"ea",I:"ightg",J:"wh"},_={OiceXe:"f0f8ff",antiquewEte:"faebd7",aqua:"ffff",aquamarRe:"7fffd4",azuY:"f0ffff",beige:"f5f5dc",bisque:"ffe4c4",black:"0",blanKedOmond:"ffebcd",Xe:"ff",XeviTet:"8a2be2",bPwn:"a52a2a",burlywood:"deb887",caMtXe:"5f9ea0",KartYuse:"7fff00",KocTate:"d2691e",cSO:"ff7f50",cSnflowerXe:"6495ed",cSnsilk:"fff8dc",crimson:"dc143c",cyan:"ffff",xXe:"8b",xcyan:"8b8b",xgTMnPd:"b8860b",xWay:"a9a9a9",xgYF:"6400",xgYy:"a9a9a9",xkhaki:"bdb76b",xmagFta:"8b008b",xTivegYF:"556b2f",xSange:"ff8c00",xScEd:"9932cc",xYd:"8b0000",xsOmon:"e9967a",xsHgYF:"8fbc8f",xUXe:"483d8b",xUWay:"2f4f4f",xUgYy:"2f4f4f",xQe:"ced1",xviTet:"9400d3",dAppRk:"ff1493",dApskyXe:"bfff",dimWay:"696969",dimgYy:"696969",dodgerXe:"1e90ff",fiYbrick:"b22222",flSOwEte:"fffaf0",foYstWAn:"228b22",fuKsia:"ff00ff",gaRsbSo:"dcdcdc",ghostwEte:"f8f8ff",gTd:"ffd700",gTMnPd:"daa520",Way:"808080",gYF:"8000",gYFLw:"adff2f",gYy:"808080",honeyMw:"f0fff0",hotpRk:"ff69b4",RdianYd:"cd5c5c",Rdigo:"4b0082",ivSy:"fffff0",khaki:"f0e68c",lavFMr:"e6e6fa",lavFMrXsh:"fff0f5",lawngYF:"7cfc00",NmoncEffon:"fffacd",ZXe:"add8e6",ZcSO:"f08080",Zcyan:"e0ffff",ZgTMnPdLw:"fafad2",ZWay:"d3d3d3",ZgYF:"90ee90",ZgYy:"d3d3d3",ZpRk:"ffb6c1",ZsOmon:"ffa07a",ZsHgYF:"20b2aa",ZskyXe:"87cefa",ZUWay:"778899",ZUgYy:"778899",ZstAlXe:"b0c4de",ZLw:"ffffe0",lime:"ff00",limegYF:"32cd32",lRF:"faf0e6",magFta:"ff00ff",maPon:"800000",VaquamarRe:"66cdaa",VXe:"cd",VScEd:"ba55d3",VpurpN:"9370db",VsHgYF:"3cb371",VUXe:"7b68ee",VsprRggYF:"fa9a",VQe:"48d1cc",VviTetYd:"c71585",midnightXe:"191970",mRtcYam:"f5fffa",mistyPse:"ffe4e1",moccasR:"ffe4b5",navajowEte:"ffdead",navy:"80",Tdlace:"fdf5e6",Tive:"808000",TivedBb:"6b8e23",Sange:"ffa500",SangeYd:"ff4500",ScEd:"da70d6",pOegTMnPd:"eee8aa",pOegYF:"98fb98",pOeQe:"afeeee",pOeviTetYd:"db7093",papayawEp:"ffefd5",pHKpuff:"ffdab9",peru:"cd853f",pRk:"ffc0cb",plum:"dda0dd",powMrXe:"b0e0e6",purpN:"800080",YbeccapurpN:"663399",Yd:"ff0000",Psybrown:"bc8f8f",PyOXe:"4169e1",saddNbPwn:"8b4513",sOmon:"fa8072",sandybPwn:"f4a460",sHgYF:"2e8b57",sHshell:"fff5ee",siFna:"a0522d",silver:"c0c0c0",skyXe:"87ceeb",UXe:"6a5acd",UWay:"708090",UgYy:"708090",snow:"fffafa",sprRggYF:"ff7f",stAlXe:"4682b4",tan:"d2b48c",teO:"8080",tEstN:"d8bfd8",tomato:"ff6347",Qe:"40e0d0",viTet:"ee82ee",JHt:"f5deb3",wEte:"ffffff",wEtesmoke:"f5f5f5",Lw:"ffff00",LwgYF:"9acd32"};let M;function X(e){M||(M=function(){const e={},t=Object.keys(_),f=Object.keys(F);let r,a,n,s,i;for(r=0;r<t.length;r++){for(s=i=t[r],a=0;a<f.length;a++)n=f[a],i=i.replace(n,F[n]);n=parseInt(_[s],16),e[i]=[n>>16&255,n>>8&255,255&n]}return e}(),M.transparent=[0,0,0,0]);const t=M[e.toLowerCase()];return t&&{r:t[0],g:t[1],b:t[2],a:4===t.length?t[3]:255}}const O=/^rgba?\(\s*([-+.\d]+)(%)?[\s,]+([-+.e\d]+)(%)?[\s,]+([-+.e\d]+)(%)?(?:[\s,/]+([-+.e\d]+)(%)?)?\s*\)$/;const S=e=>e<=.0031308?12.92*e:1.055*Math.pow(e,1/2.4)-.055,T=e=>e<=.04045?e/12.92:Math.pow((e+.055)/1.055,2.4);function Z(e,t,f){if(e){let r=Y(e);r[t]=Math.max(0,Math.min(r[t]+r[t]*f,0===t?360:1)),r=w(r),e.r=r[0],e.g=r[1],e.b=r[2]}}function $(e,t){return e?Object.assign(t||{},e):e}function E(e){var t={r:0,g:0,b:0,a:255};return Array.isArray(e)?e.length>=3&&(t={r:e[0],g:e[1],b:e[2],a:255},e.length>3&&(t.a=s(e[3]))):(t=$(e,{r:0,g:0,b:0,a:1})).a=s(t.a),t}function R(e){return"r"===e.charAt(0)?function(e){const t=O.exec(e);let f,r,s,i=255;if(t){if(t[7]!==f){const e=+t[7];i=t[8]?n(e):a(255*e,0,255)}return f=+t[1],r=+t[3],s=+t[5],f=255&(t[2]?n(f):a(f,0,255)),r=255&(t[4]?n(r):a(r,0,255)),s=255&(t[6]?n(s):a(s,0,255)),{r:f,g:r,b:s,a:i}}}(e):k(e)}class A{constructor(e){if(e instanceof A)return e;const t=typeof e;let f;var r,a,n;"object"===t?f=E(e):"string"===t&&(n=(r=e).length,"#"===r[0]&&(4===n||5===n?a={r:255&17*b[r[1]],g:255&17*b[r[2]],b:255&17*b[r[3]],a:5===n?17*b[r[4]]:255}:7!==n&&9!==n||(a={r:b[r[1]]<<4|b[r[2]],g:b[r[3]]<<4|b[r[4]],b:b[r[5]]<<4|b[r[6]],a:9===n?b[r[7]]<<4|b[r[8]]:255})),f=a||X(e)||R(e)),this._rgb=f,this._valid=!!f}get valid(){return this._valid}get rgb(){var e=$(this._rgb);return e&&(e.a=i(e.a)),e}set rgb(e){this._rgb=E(e)}rgbString(){return this._valid?(e=this._rgb)&&(e.a<255?`rgba(${e.r}, ${e.g}, ${e.b}, ${i(e.a)})`:`rgb(${e.r}, ${e.g}, ${e.b})`):void 0;var e}hexString(){return this._valid?h(this._rgb):void 0}hslString(){return this._valid?function(e){if(!e)return;const t=Y(e),f=t[0],r=c(t[1]),a=c(t[2]);return e.a<255?`hsla(${f}, ${r}%, ${a}%, ${i(e.a)})`:`hsl(${f}, ${r}%, ${a}%)`}(this._rgb):void 0}mix(e,t){if(e){const f=this.rgb,r=e.rgb;let a;const n=t===a?.5:t,s=2*n-1,i=f.a-r.a,c=((s*i==-1?s:(s+i)/(1+s*i))+1)/2;a=1-c,f.r=255&c*f.r+a*r.r+.5,f.g=255&c*f.g+a*r.g+.5,f.b=255&c*f.b+a*r.b+.5,f.a=n*f.a+(1-n)*r.a,this.rgb=f}return this}interpolate(e,t){return e&&(this._rgb=function(e,t,f){const r=T(i(e.r)),a=T(i(e.g)),n=T(i(e.b));return{r:s(S(r+f*(T(i(t.r))-r))),g:s(S(a+f*(T(i(t.g))-a))),b:s(S(n+f*(T(i(t.b))-n))),a:e.a+f*(t.a-e.a)}}(this._rgb,e._rgb,t)),this}clone(){return new A(this.rgb)}alpha(e){return this._rgb.a=s(e),this}clearer(e){return this._rgb.a*=1-e,this}greyscale(){const e=this._rgb,t=r(.3*e.r+.59*e.g+.11*e.b);return e.r=e.g=e.b=t,this}opaquer(e){return this._rgb.a*=1+e,this}negate(){const e=this._rgb;return e.r=255-e.r,e.g=255-e.g,e.b=255-e.b,this}lighten(e){return Z(this._rgb,2,e),this}darken(e){return Z(this._rgb,2,-e),this}saturate(e){return Z(this._rgb,1,e),this}desaturate(e){return Z(this._rgb,1,-e),this}rotate(e){return function(e,t){var f=Y(e);f[0]=x(f[0]+t),f=w(f),e.r=f[0],e.g=f[1],e.b=f[2]}(this._rgb,e),this}}}}]);