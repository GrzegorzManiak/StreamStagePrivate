(()=>{"use strict";function t(t,i){var r="undefined"!=typeof Symbol&&t[Symbol.iterator]||t["@@iterator"];if(!r){if(Array.isArray(t)||(r=function(t,i){if(!t)return;if("string"==typeof t)return e(t,i);var r=Object.prototype.toString.call(t).slice(8,-1);"Object"===r&&t.constructor&&(r=t.constructor.name);if("Map"===r||"Set"===r)return Array.from(t);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return e(t,i)}(t))||i&&t&&"number"==typeof t.length){r&&(t=r);var a=0,n=function(){};return{s:n,n:function(){return a>=t.length?{done:!0}:{done:!1,value:t[a++]}},e:function(t){throw t},f:n}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var s,o=!0,l=!1;return{s:function(){r=r.call(t)},n:function(){var t=r.next();return o=t.done,t},e:function(t){l=!0,s=t},f:function(){try{o||null==r.return||r.return()}finally{if(l)throw s}}}}function e(t,e){(null==e||e>t.length)&&(e=t.length);for(var i=0,r=new Array(e);i<e;i++)r[i]=t[i];return r}var i=document.getElementById("thumbnail");function r(t){var e=i.cloneNode(!0);e.id="thumbnail-"+t.id,e.setAttribute("data-is-live",t.is_live.toString()),e.setAttribute("data-is-hidden","false"),e.setAttribute("data-is-skeleton","false");e.querySelector('[data-elm="main-image"]'),e.querySelector('[data-elm="pfp"]');var r=e.querySelector('[data-elm="title"]'),a=e.querySelector('[data-elm="view-count"]'),n=e.querySelector('[data-elm="date-vod"]');return r.innerText=t.title,a.innerText=t.views_formatted,n.innerText=t.start_time,e}i.id="";var a={id:"1",name:"Test Streamer",pfp:"https://via.placeholder.com/300x300"};!function(e,i){var a=function(e,i){for(var a=[],n=0;n<3;n++){for(var s=[],o=0;o<6;o++){var l=i[Math.floor(Math.random()*i.length)];s.push(l)}a.push(s)}for(var d=0,m=a;d<m.length;d++){var c=m[d];if(c.length<3)for(var v=3-c.length,u=0;u<v;u++){var p=i[Math.floor(Math.random()*i.length)];a[u].push(p)}}for(var h=[],f=0,_=a;f<_.length;f++){var T=_[f],w=document.createElement("div");w.classList.add("carousel-group");var b,y=t(T);try{for(y.s();!(b=y.n()).done;){var g=r(b.value);w.appendChild(g)}}catch(t){y.e(t)}finally{y.f()}h.push(w)}for(var x=0,S=h;x<S.length;x++){var D=S[x];e.appendChild(D)}return{content:a,groups:h}}(e,i);a.content,a.groups}(document.querySelector("#carousel"),[{id:"1",is_live:!1,title:"Test Title 1",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:a},{id:"2",is_live:!0,title:"Test Title 2",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:a},{id:"3",is_live:!0,title:"Test Title 3",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:a},{id:"4",is_live:!1,title:"Test Title 4",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:a},{id:"5",is_live:!1,title:"Test Title 5",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:a},{id:"6",is_live:!0,title:"Test Title 6",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:a},{id:"7",is_live:!1,title:"Test Title 7",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:a},{id:"8",is_live:!0,title:"Test Title 8",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:a},{id:"9",is_live:!1,title:"Test Title 9",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:a},{id:"10",is_live:!1,title:"Test Title 0",views:100,views_formatted:"100",description:"Test Description",start_time:"2020-01-01",end_time:"2020-01-01",thumbnail:"https://via.placeholder.com/300x300",streamer:a}])})();