import React, {useEffect, useRef, useState} from 'react';
import Feed from '../../Chatbox/Feed/feed';
import "./burgerstyle.css";
import Popup from "../../popup/popup"
import func from "../../Language/Lanprocess";
function Burger (){
    const [open, setopen] = useState(false);//the state for if the menu bar is open or not
    const [popupmenu, setpopupmenu] = useState(false);//this states keeps track of if help is needed.
    const [popupmessage,setpopupmessage] = useState(null);
    let menuRef = useRef();
    let helpRef = useRef();
    useEffect(()=>{
        let handler = (Event)=>{
            if(!popupmenu && !menuRef.current.contains(Event.target))//check if the menu is open and the click is not on the menu
                setopen(false);
            else if(popupmenu && !helpRef.current.contains(Event.target))//checks if we are on help and if the click is not on the box
                setpopupmenu(false);
        }
        document.addEventListener("mousedown",handler);

        return () =>{
            document.removeEventListener("mousedown",handler);
        }
    },[open,popupmenu]);
    return (
        <>
        {popupmenu && <Popup message={popupmessage} setstate={setpopupmenu} helpref= {helpRef}/>}
        <div ref={menuRef}>
        <div  className= {!open?'container':'container change'} onClick={()=>setopen((open)=>!open)}>
            <div className='bar1'></div>
            <div className='bar2'></div>
            <div className='bar3'></div>
        </div>
        <div ref={menuRef} className={!open?'closed':'open'}>
            <Dropdownmenu state={popupmenu} func ={setpopupmenu} setmessage = {setpopupmessage}/>
        </div>
        </div>
        </>
    );
}
function disclaimer(state, setstate,setMessage){
    setstate(!state);
    setMessage([func("disclaimermenu"),func("disclaimertext")]);
}
function HelpButton (state , setstate , setMessage) {
    setstate(!state);
    setMessage([func("mainhelpmenu"),func("helptext")]);
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
            <DropdownItem act = {()=>HelpButton(props.state, props.func , props.setmessage)}><div>{func("helpmenu")}</div></DropdownItem>      
            <DropdownItem act ={()=>disclaimer(props.state,props.func,props.setmessage)}><div>{func("disclaimermenu")}</div></DropdownItem>
            <DropdownItem act = {changecolor}><div>{func("switchbutton")}</div></DropdownItem>
        </div>
        </>
    );
}
export default Burger;