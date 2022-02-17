import React from "react";
import "./dropdownmenu.css";

function fontSize(){

}

function Dropdownmenu(){
        function DropdownItem(props){
            return(
                <div>
                    {props.children}
                </div>
            )
        }
        return (
            <div className='dropdown'>
                <DropdownItem>My test</DropdownItem>
                <DropdownItem>test again</DropdownItem>
                <DropdownItem>tt</DropdownItem>
                <DropdownItem>t<button onClick={fontSize}>bt</button></DropdownItem>
                
            </div>
        );
    }
export default Dropdownmenu;