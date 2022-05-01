import React from 'react';
import "./clipbutton.css";
import clipboard from "./clipboard.svg"
async function myfunc(messages){
    var s = "";
    messages.forEach(message => {
        s = s + message["props"]["type"] + " : "+ message["props"]["text"] + "\n\n";
    });
    await navigator.clipboard.writeText(s);
    alert("Text is copied to clipboard.");
}

function ClipButton(props){
    return(
        <button className='clip-button' onClick={()=>myfunc(props.messages)}>
            <img src = {clipboard} alt="clipboard"></img>
        </button>
    );
}
export default ClipButton;