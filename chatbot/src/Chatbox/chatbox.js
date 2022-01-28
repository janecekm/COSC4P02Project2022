import React, {useState} from 'react';
import "./chatbox.css"
import Feed from './Feed/feed';
import Form from './Form/form';
import ClearButton from './ClearButton/clear';
import EnterButton from './EnterButton/enter';

function Chatbox(){
    return(
        
        <div className='Chatbox'>

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