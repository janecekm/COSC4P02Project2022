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
    
    var temp = window.location.href.toString();
    var v = temp.search("/canada");
    if(v==-1){//in canada{//to canada
        var temp = window.location.href;
        window.location.replace("http://localhost:5000/canada");
        setstaty(false);
    }
    else{
        window.location.replace("http://localhost:5000/brock");
        setstaty(true);
    }
}
function Dropdownmenu(props){
    const [brockorcad, setbrockorcad] = useState(true);
    function DropdownItem(props){
        return(
            <div className="menuitem" onClick = {props.act}>
                {props.children}
            </div>
        )
    }

    return (
        <>
        <div className='dropdown'>
            <DropdownItem act ={helpThem}><div>Help</div></DropdownItem>
            <DropdownItem act ={fontSizeInc}><div>Font Increase</div></DropdownItem>
            <DropdownItem act ={fontSizeDec}><div>Font Decrease</div></DropdownItem>
            <DropdownItem act = {()=>changecolor(brockorcad,setbrockorcad)}><div>Switch Modes</div></DropdownItem>
        </div>
        </>
    );
}
export default Burger;