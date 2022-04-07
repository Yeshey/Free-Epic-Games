var sel = window.getSelection();
var result = "no_selection";
if (sel.rangeCount) {
    var range = sel.getRangeAt(0).cloneRange();
    if (range.getBoundingClientRect) {
        range.collapse(true);
        var rect = range.getBoundingClientRect();
        if (rect) {
            x = rect.left;
            y = rect.top;
            x += window.mozInnerScreenX;
            y += window.mozInnerScreenY;
            result = "" + x + " " + y;
        }
    }
}
navigator.clipboard.writeText(result);
