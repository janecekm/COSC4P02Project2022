import React, {useState} from 'react';
import "./chatbox.css"
import Feed from './Feed/feed';
import Clipbutton from './ClipButton/clipbutton'

function Chatbox(){
    return(
        
        <div className='Chatbox'>
            <Feed />
            
         </div>
    )
}

export default Chatbox;