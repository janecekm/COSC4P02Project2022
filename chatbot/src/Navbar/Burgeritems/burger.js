import React, {useState} from 'react';
import "./burgerstyle.css";

function Burger (){
    const [open, setopen] = useState(false);
    
    return (
        <>
        <div className= {!open?'container':'container change'} onClick={()=>setopen(!open)}>
            <div className='bar1'></div>
            <div className='bar2'></div>
            <div className='bar3'></div>
        </div>
        {open && <Dropdownmenu />}
        </>
    );
}
function fontSizeDec(){
    var temp = document.getElementById('root');
    var len = getComputedStyle(temp).getPropertyValue('--text-size').length;
    var num = parseInt(getComputedStyle(temp).getPropertyValue('--text-size').substring(0,len-2))-1;
    if (num > 9) {
        temp.style.setProperty('--text-size',num+"px");
    }
}
function fontSizeInc(){
    var temp = document.getElementById('root');
    var len = getComputedStyle(temp).getPropertyValue('--text-size').length;
    var num = parseInt(getComputedStyle(temp).getPropertyValue('--text-size').substring(0,len-2))+1;
    if (num < 26) {
        temp.style.setProperty('--text-size',num+"px");
    }
}
function helpThem () {
    alert("*HELPFUL MESSAGE*");
}
function changecolor(staty,setstaty){
    
    var temp = document.getElementById('root');
    if(staty){//brock colors
        temp.style.setProperty('--primary-color',getComputedStyle(temp).getPropertyValue('--canada-colors'));
        temp.style.setProperty('--secondary-color',getComputedStyle(temp).getPropertyValue('--canada-secondary-colors'))
        setstaty(false);
    }
    else{
        temp.style.setProperty('--primary-color',getComputedStyle(temp).getPropertyValue('--brock-colors'));
        temp.style.setProperty('--secondary-color',getComputedStyle(temp).getPropertyValue('--brock-secondary-colors'))
        setstaty(true);
    }
}
function Dropdownmenu(props){
    const [brockorcad, setbrockorcad] = useState(true);
    function DropdownItem(props){
        return(
            <div className="menuitem">
                {props.children}
            </div>
        )
    }

    return (
        <>
        <div className='dropdown'>
            <DropdownItem ><div onClick={helpThem}>Help</div></DropdownItem>
            <DropdownItem ><div onClick={fontSizeInc}>Font Increase</div></DropdownItem>
            <DropdownItem ><div onClick={fontSizeDec}>Font Decrease</div></DropdownItem>
            <DropdownItem ><div onClick={()=>changecolor(brockorcad,setbrockorcad)}>Switch Modes</div></DropdownItem>
        </div>
        </>
    );
}
export default Burger;