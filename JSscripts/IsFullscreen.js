document.addEventListener("focus", function handler(e) { 
    e.currentTarget.removeEventListener(e.type, handler);
    if(!window.screenTop && !window.screenY){
        str = "YES" 
    } else { 
        str = "NO" 
    } 
    navigator.clipboard.writeText(str); 
});    