import React, {useState} from 'react';
import "./burgerstyle.css";

function Burger (){
    const [open, setopen] = useState(false);//the state for if the menu bar is open or not
    return (
        <>
        <div className= {!open?'container':'container change'} onClick={()=>setopen(!open)}>
            <div className='bar1'></div>
            <div className='bar2'></div>
            <div className='bar3'></div>
        </div>
        <div className={!open?'closed':'open'}>
            <Dropdownmenu />
        </div>
       
        </>
    );
}
function fontSizeDec(){
    var temp = document.getElementById('root');
    var len = getComputedStyle(temp).getPropertyValue('--text-size').length;
    var num = parseInt(getComputedStyle(temp).getPropertyValue('--text-size').substring(0,len-2))-1;
    var th = parseInt(getComputedStyle(temp).getPropertyValue('--thinking-size')) -1;
    if (num > 9) {//the smallest size of the alphabets
        temp.style.setProperty('--text-size',num+"px");
        temp.style.setProperty('--thinking-size',th+"px");
    }
}
function fontSizeInc(){
    var temp = document.getElementById('root');
    var len = getComputedStyle(temp).getPropertyValue('--text-size').length;
    var num = parseInt(getComputedStyle(temp).getPropertyValue('--text-size').substring(0,len-2))+1;
    var th = parseInt(getComputedStyle(temp).getPropertyValue('--thinking-size')) +1;
    if (num < 26) {//the largest size of the alphabets 
        temp.style.setProperty('--text-size',num+"px");//changes the size of the text
        temp.style.setProperty('--thinking-size',th +"px");//changes the size of the thinking animation
    }
}
function HelpButton () {
    alert("*HELPFUL MESSAGE*");
}
function changecolor(){
    
    var url = window.location.href.toString();
    var isCanada = url.search("/canada");
    if(isCanada===-1){//if we are in the brock's website
        let link = url.replace("brock", "canada");
        window.location.replace(link);
    }
    else{
        let link = url.replace("canada", "brock")
        window.location.replace(link);
    }
}
/**
 * 
 * @param {the content of each item in menu bar} props 
 * @returns the <div> object for the menu bar
 */
function Dropdownmenu(props){
    function DropdownItem(props){
        return(
            <div className="menuitem" onClick = {props.act}>
                {props.children}
            </div>
        )
    }

    return (
        <>
        <div className= "dropdown">
            <DropdownItem act ={HelpButton}><div>Help</div></DropdownItem>
            <DropdownItem act ={fontSizeInc}><div>Font +</div></DropdownItem>
            <DropdownItem act ={fontSizeDec}><div>Font -</div></DropdownItem>
            <DropdownItem act = {changecolor}><div>Switch</div></DropdownItem>
        </div>
        </>
    );
}
export default Burger;