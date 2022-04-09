import React from "react";
import "./popup.css"
import func from "../Language/Lanprocess"
function Popup(props){
  return (
  <div className="popup-box">
    <div className="box">
      <button className="close-icon" onClick={()=>props.setstate(false)}>X</button>
      <div className="popup-title">Help menu</div>
      <div className="popup-content">{func("help")}</div>
    </div>
  </div>
  )
}
 
export default Popup;