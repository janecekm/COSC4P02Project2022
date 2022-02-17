import React from "react";
import "./backarrowdesign.css";
import Backarrowimage from './backarrowimage.svg';
function Backarrowbutton(){
    return(
        <div className="arrow">
              <img src = {Backarrowimage} alt="backarrow"></img>
        </div>
    )
}
export default Backarrowbutton;