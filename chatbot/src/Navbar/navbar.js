import React, {useState} from 'react';
import "./Navbardesign.css"
import Burger from './Burgeritems/burger';
import Backarrowbutton from './backarrow/backarrowbutton';
import func from "../Language/Lanprocess";

function Navbar(){
    return(
        
        <div className='Navbar'>

         <div className='Backarrow'>
                    
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