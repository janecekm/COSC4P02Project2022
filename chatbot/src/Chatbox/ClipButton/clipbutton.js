import React, {useState} from 'react';
import "./clipbutton.css";
import clipboard from "./clipboard.svg"
function myfunc(){
    console.log("pushed");
}

function ClipButton(){
    return(
        <button className='clip-button' onClick={myfunc}>
            <img src = {clipboard} alt="clipboard"></img>
        </button>
    );
}
export default ClipButton;