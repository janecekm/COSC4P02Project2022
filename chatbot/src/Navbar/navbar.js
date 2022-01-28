import React, {useState} from 'react';
import "./Navbardesign.css"
import Burger from './Burgeritems/burger';
import Backarrowbutton from './backarrow/backarrowbutton';

function Navbar(){
    const [open,setOpen] = useState(false);
    return(
        
        <div className='Navbar'>

         <div className='Backarrow'>
                    <Backarrowbutton />
            </div>
            <div className='ChatbotName'>
                    Chatbotname here
            </div>
            <div className= 'BurgerMenu'>
                <Burger open = {open} setOpen={setOpen}/>
            </div>
            
            </div>
    )
}

export default Navbar;