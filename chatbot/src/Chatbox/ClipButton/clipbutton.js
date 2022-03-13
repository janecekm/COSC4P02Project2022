import React from 'react';
import "./clipbutton.css";
import clipboard from "./clipboard.svg"
function myfunc(messages){
    var s = "";
    messages.forEach(message => {
        s = s + message["props"]["type"] + " : "+ message["props"]["text"];
        if(message["props"]["type"] === "response")
        s = s+"\n";
    });
    navigator.clipboard.writeText(s);
    alert("text is copied");
}

function ClipButton(props){
    return(
        <button className='clip-button' onClick={()=>myfunc(props.messages)}>
            <img src = {clipboard} alt="clipboard"></img>
        </button>
    );
}
export default ClipButton;