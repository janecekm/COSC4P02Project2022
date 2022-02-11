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
    temp.style.setProperty('--text-size',num+"px");
    console.log(num);
}
function fontSizeInc(){
    var temp = document.getElementById('root');
    var len = getComputedStyle(temp).getPropertyValue('--text-size').length;
    var num = parseInt(getComputedStyle(temp).getPropertyValue('--text-size').substring(0,len-2))+1;
    temp.style.setProperty('--text-size',num+"px");
    console.log(num);
}
function changecolor(staty,setstaty){
    
    var temp = document.getElementById('root');
    if(staty){//brock colors
        temp.style.setProperty('--primary-color',getComputedStyle(temp).getPropertyValue('--canada-colors'));
        setstaty(false);
    }
    else{
        temp.style.setProperty('--primary-color',getComputedStyle(temp).getPropertyValue('--brock-colors'));
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
            <DropdownItem >item1</DropdownItem>
            <DropdownItem>item2</DropdownItem>
            <DropdownItem ><div onClick={fontSizeInc}>font inc</div></DropdownItem>
            <DropdownItem ><div onClick={fontSizeDec}>font dec</div></DropdownItem>
            <DropdownItem ><div onClick={()=>changecolor(brockorcad,setbrockorcad)}>change team</div></DropdownItem>
        </div>
        </>
    );
}
export default Burger;