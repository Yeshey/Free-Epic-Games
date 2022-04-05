if(!window.screenTop && !window.screenY){
    str = "YES" 
} else { 
    str = "NO" 
} 
navigator.clipboard.writeText(str); 