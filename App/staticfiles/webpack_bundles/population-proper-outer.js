"use strict";(self.webpackChunk=self.webpackChunk||[]).push([[936],{936:(n,e,t)=>{function a(n){var e=!(arguments.length>1&&void 0!==arguments[1])||arguments[1],t=!(arguments.length>2&&void 0!==arguments[2])||arguments[2],a="\n <div class='w-100'>\n <div class='event d-flex justify-content-between align-items-center w-100'>\n <p class='event-title'>".concat(n.event_name,"</p>\n <p class='event-rating'>").concat(n.rating," / 5</p>\n <p class='event-likes'>").concat(n.likes," ").concat(1===n.likes?"like":"likes","</p>\n <p class='event-date'>").concat(new Date(n.created).toLocaleDateString(),"</p>\n </div>\n <hr>\n <div class='d-flex justify-content-between align-items-start w-100 flex-column'>\n <p class='review-title'><span class='title'>").concat(n.title,"</span> <span class='text-muted you'>- ").concat(t?"You":"@"+n.username,"</span></p>\n <p class='review-body'>").concat(n.body,"</p>\n </div>\n </div>\n\n ").concat(e?" \n <div class='btn-container d-flex justify-content-end align-items-center flex-column gap-2 h-100 flex-grow-0'>\n <button \n data-review-id='".concat(n.id,"'\n class=\"w-100 h-100 btn btn-primary btn-lg info loader-btn edit-review-btn review-btn\"\n loader-state='default'> <span> <div class='spinner-border' role='status'> \n <span class='visually-hidden'>Loading...</span> </div> </span>\n <p>Edit</p>\n </button>\n\n <button \n data-review-id='").concat(n.id,"'\n class=\"w-100 h-100 btn btn-danger btn-lg error loader-btn remove-review-btn review-btn\"\n loader-state='default'> <span> <div class='spinner-border' role='status'> \n <span class='visually-hidden'>Loading...</span> </div> </span>\n <p>Delete</p>\n </button>\n </div>\n "):"","\n "),s=document.createElement("div");return s.classList.add("review","d-flex","justify-content-between","align-items-center","w-100","gap-2"),s.innerHTML=a,s}t.d(e,{I:()=>a})}}]);