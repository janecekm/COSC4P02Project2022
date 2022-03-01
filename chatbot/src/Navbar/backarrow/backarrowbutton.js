import React from "react";
import "./backarrowdesign.css";
import Backarrowimage from './backarrowimage.svg';
function Backarrowbutton(){


    const goBack = () => {
        window.location.replace("http://localhost:5000");
    }

    return(
        <div className="arrow">
              <img src = {Backarrowimage} alt="backarrow" 
              onClick={goBack}></img>
        </div>
    )
}
export default Backarrowbutton;