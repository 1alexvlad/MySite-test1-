// проверяет не был ли букмарклет уже загружен
(function(){
    if(!window.bookmarklet) {
        bookmarklet_js = document.body.appendChild(document.
        createElement('script'));
//  Атрибут src используется для загрузки URL-адреса со случайным значением. Если букмарклета был загружен ранее, то другое значение данного параметра заставит браузер снова загрузить
// скрипт с исходного URL-адреса. При таком подходе мы обеспечиваем,чтобы букмарклет всегда запускал самый актуальный исходный код
        bookmarklet_js.src = '//127.0.0.1:8000/static/js/bookmarklet.js?r='+ Math.floor(Math.random()*9999999999999999);
        window.bookmarklet = true;
    }
    else {
        bookmarkletLaunch();
    }
})();
   