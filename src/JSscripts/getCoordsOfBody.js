var list = document.body
var rect = list.getBoundingClientRect();
console.log(rect.top, rect.right, rect.bottom, rect.left);

// https://stackoverflow.com/questions/442404/retrieve-the-position-x-y-of-an-html-element
/*
var bodyRect = document.body.getBoundingClientRect(),
    elemRect = document.querySelector("button").getBoundingClientRect(),
    offset   = elemRect.top - bodyRect.top;

    console.log(document.querySelector("button").getBoundingClientRect())
    console.log(document.body.getBoundingClientRect())
    //alert('Element is ' + offset + ' vertical pixels from <body>');
*/

/*
// get cords of element
var list = document.querySelectorAll("button");
for (var i=0; i<list.length; i++){
    var rect = list[i].getBoundingClientRect();
    console.log(rect.top, rect.right, rect.bottom, rect.left);
}
*/