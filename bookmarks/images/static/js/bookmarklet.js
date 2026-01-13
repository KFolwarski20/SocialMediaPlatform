(function(){
    var jquery_version = '3.3.1';
    var site_url = 'http://127.0.0.1:8000/';
    var static_url = site_url + 'static/';
    var min_width = 100;

    function bookmarklet(msg) {
        // Wczytanie stylów CSS.
        var css = jQuery('<link>');
        css.attr({
            rel: 'stylesheet',
            type: 'text/css',
            href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random()*99999999999999999999)
        });
        jQuery('head').append(css);
        // Wczytanie kodu HTML.
        box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a>' +
            '<h1>Wybierz obraz do dodania:</h1><div class="images"></div></div>';
        jQuery('body').append(box_html);
        // Zdarzenie losowe.
        jQuery('#bookmarklet #close').click(function(){
            jQuery('#bookmarklet').remove();
        });
    };
    // Sprawdzenie czy biblioteka jQuery została wczytana.
    if (typeof window.jQuery != 'undefined'){
        bookmarklet();
    } else {
        // Sprawdzenie pod kątem konfliktów.
        var conflict = typeof window.$ != 'undefined';
        // Utworzenie skryptu i wskazanie API Google.
        var script = document.createElement('script');
        script.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/' +
            jquery_version + '/jquery.min.js');
        // Dodanie znacznika skryptu do znacznika <head> w celu przetworzenia.
        document.getElementsByTagName('head')[0].appendChild(script);
        // Mechanizm pozwalający na zaczekanie aż do zakończenia wczytywania skryptu.
        var attempts = 15;
        (function(){
            // Ponownie sprawdzamy czy zdefiniowano jQuery.
            if (typeof window.jQuery == 'undefined'){
                if (--attempts > 0){
                    //Wywołanie skryptu w ciągu kilku milisekund.
                    window.setTimeout(arguments.callee, 250)
                } else {
                    // Zbyt wiele prób wczytania, zgłoszenie błędu.
                    alert("Wystąpił błąd podczas wczytywania jQuery.")
                }
            } else {
                bookmarklet();
            }
        })();
    }
})()