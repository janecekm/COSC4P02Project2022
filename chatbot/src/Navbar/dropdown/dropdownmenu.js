import React from "react";
import "./dropdownmenu.css";

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
            </div>
        );
    }
export default Dropdownmenu;