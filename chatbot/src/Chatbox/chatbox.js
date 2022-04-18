import React from 'react';
import "./chatscreen.css"
import Feed from './Feed/feed';


function Chatbox(){
    
    return(
        <div className='Chatbox'>
            <div className='Chatbot'>
                <Feed />
            </div>
         </div>
    )
}

export default Chatbox;