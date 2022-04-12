import React, {useEffect, useRef, useState} from 'react';
import Feed from '../../Chatbox/Feed/feed';
import "./burgerstyle.css";
import Popup from "../../popup/popup"
import 'reactjs-popup/dist/index.css';
import func from "../../Language/Lanprocess";
function Burger (){
    const [open, setopen] = useState(false);//the state for if the menu bar is open or not
    const [help, sethelp] = useState(false);//this states keeps track of if help is needed.
    let menuRef = useRef();
    let helpRef = useRef();
    useEffect(()=>{
        let handler = (Event)=>{
            if(!help && !menuRef.current.contains(Event.target))//check if the menu is open and the click is not on the menu
                setopen(false);
            else if(help && !helpRef.current.contains(Event.target))//checks if we are on help and if the click is not on the box
                sethelp(false);
        }
        document.addEventListener("mousedown",handler);

        return () =>{
            document.removeEventListener("mousedown",handler);
        }
    },[open,help]);
    return (
        <>
        {help && <Popup setstate={sethelp} helpref= {helpRef}/>}
        <div ref={menuRef}>
        <div  className= {!open?'container':'container change'} onClick={()=>setopen((open)=>!open)}>
            <div className='bar1'></div>
            <div className='bar2'></div>
            <div className='bar3'></div>
        </div>
        <div ref={menuRef} className={!open?'closed':'open'}>
            <Dropdownmenu helpstate={help} helpfunc ={sethelp}/>
        </div>
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
function HelpButton (state , setstate) {
    console.log(state);
    setstate(!state);
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
            <DropdownItem act = {()=>HelpButton(props.helpstate, props.helpfunc)}><div>Help</div></DropdownItem>      
            <DropdownItem act ={fontSizeInc}><div>Font +</div></DropdownItem>
            <DropdownItem act ={fontSizeDec}><div>Font -</div></DropdownItem>
            <DropdownItem act = {changecolor}><div>Switch</div></DropdownItem>
        </div>
        </>
    );
}
export default Burger;