import React from "react";
import "./backarrowdesign.css";
import Backarrowimage from './backarrowimage.svg';
function Backarrowbutton(){


    const goBack = () => {
        link = window.location.href
        link = link.replace("brock", "")
        link = link.replace("canada", "")
        window.location.replace(link);
    }

    return(
        <div className="arrow">
              <img src = {Backarrowimage} alt="backarrow" 
              onClick={goBack}></img>
        </div>
    )
}
export default Backarrowbutton;