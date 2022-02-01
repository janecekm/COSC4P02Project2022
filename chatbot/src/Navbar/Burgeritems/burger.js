import React, {useState} from 'react';
import "./burgerstyle.css"
import Dropdownmenu from '../dropdown/dropdownmenu';

function Burger (){
    const [open, setopen] = useState(false);
    return (
        <>
        <div className= {!open?'container':'container change'} onClick={()=>setopen(!open)}>
            <div className='bar1'></div>
            <div className='bar2'></div>
            <div className='bar3'></div>
        </div>
        <Dropdownmenu state = {open}/>
        </>
    );
}
export default Burger;