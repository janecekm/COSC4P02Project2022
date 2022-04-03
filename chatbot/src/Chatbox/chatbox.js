import React from 'react';
import "./chatbox.css"
import Feed from './Feed/feed';

function Chatbox(props){
    console.log(props);
    return(
        <div className='Chatbox'>
            <Feed />
         </div>
    )
}

export default Chatbox;