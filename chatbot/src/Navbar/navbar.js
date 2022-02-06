import React, {useState} from 'react';
import "./Navbardesign.css"
import Burger from './Burgeritems/burger';
import Backarrowbutton from './backarrow/backarrowbutton';

function Navbar(){
    return(
        
        <div className='Navbar'>

         <div className='Backarrow'>
                    
            </div>
            <div className='ChatbotName'>
                    BrockBot
            </div>
            <div className= 'BurgerMenu'>
                <Burger />       
            </div>
            
        </div>
    )
}

export default Navbar;