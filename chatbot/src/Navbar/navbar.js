import React from 'react';
import "./Navbardesign.css"
import Burger from './Burgeritems/burger';
import func from "../Language/Lanprocess";
import Backarrowbutton from './backarrow/backarrowbutton'
import image from "./noborderbadger.png"

function Navbar(){//this is the navbar component
    return(
        <div className='Navbar'>

            <div className='Backarrow'>
                <Backarrowbutton />
            </div>

            <div className='ChatbotName'>
                    <img className='badger' src= {image} width='45rem' />
                    {func("name")}  
                                   
            </div>

            <div className= 'BurgerMenu'>
                <Burger />       
            </div>

        </div>
    )
}

export default Navbar;