import React, {useState} from 'react';
import "./Navbardesign.css"
import Burger from './Burgeritems/burger';
import func from "../Language/Lanprocess";
import Backarrowbutton from './backarrow/backarrowbutton'

function Navbar(){
    
    return(
        
        <div className='Navbar'>

            <div className='Backarrow'>
                <Backarrowbutton />
            </div>
            
            <div className='ChatbotName'>
                    {func("name")}
            </div>
            <div className= 'BurgerMenu'>
                <Burger />       
            </div>
            
        </div>
    )
}

export default Navbar;