// https://stackoverflow.com/questions/7083693/detect-if-page-has-finished-loading
if (document.readyState === "complete"){
    navigator.clipboard.writeText("loaded");
} else {
    window.onload = function () { 
        navigator.clipboard.writeText("loaded");
    }
}
/*
if (document.readyState === "complete"){
    alert("loaded");
} else {
    window.onload = function () { 
        alert("loaded");
    }
}

document.onreadystatechange = () => {
    if (document.readyState === 'complete') {
        alert("loaded");
    }
};
*/