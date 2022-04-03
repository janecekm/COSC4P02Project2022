import React from 'react';
import "./chatbox.css"
import Feed from './Feed/feed';
function test(){
    console.log("what is happening?");
}

function Chatbox(){
    
    return(
        <div className='Chatbox'>
            <Feed />
         </div>
    )
}

export default Chatbox;