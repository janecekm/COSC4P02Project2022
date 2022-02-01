import React, {useState} from 'react';
import "./chatbox.css"
import Feed from './Feed/feed';
import Form from './Form/form';
import ClearButton from './ClearButton/clear';
import EnterButton from './EnterButton/enter';
import Clipbutton from './ClipButton/clipbutton';

function Chatbox(){
    return(
        
        <div className='Chatbox'>
            <Clipbutton />
            <Feed />
            <Form />
            <div className='Buttons'>
                 <ClearButton/>
                 <EnterButton/>

            </div>
         </div>
    )
}

export default Chatbox;