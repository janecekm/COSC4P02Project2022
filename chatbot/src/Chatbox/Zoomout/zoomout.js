import React from "react";
import "../ClipButton/clipbutton.css"
function fontSizeDec(){
    var temp = document.getElementById('root');
    var len = getComputedStyle(temp).getPropertyValue('--text-size').length;
    var num = parseInt(getComputedStyle(temp).getPropertyValue('--text-size').substring(0,len-2))-1;
    var th = parseInt(getComputedStyle(temp).getPropertyValue('--thinking-size')) -1;
    if (num > 9) {//the smallest size of the alphabets
        temp.style.setProperty('--text-size',num+"px");
        temp.style.setProperty('--thinking-size',th+"px");
    }
}

function Zoomout(){
    return(
        <button className="clip-button" onClick={fontSizeDec}>
            <svg xmlns="http://www.w3.org/2000/svg" width="42" height="52" fill="currentColor" class="bi bi-zoom-out" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z"/>
  <path d="M10.344 11.742c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1 6.538 6.538 0 0 1-1.398 1.4z"/>
  <path fill-rule="evenodd" d="M3 6.5a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1-.5-.5z"/>
</svg>
        </button>
    );
}

export default Zoomout;