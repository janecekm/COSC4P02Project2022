import React, {useState} from 'react';
import "./chatbox.css"
import Feed from './Feed/feed';

function Chatbox(){
    return(
        
        <div className='Chatbox'>
            <Clipbutton />
            <Feed />
            
         </div>
    )
}

export default Chatbox;