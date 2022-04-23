import React from "react";
import "./popUp.css"
import func from "../Language/Lanprocess"
function Popup(props){
  return (
  <div className="popup-box">
    <div ref={props.helpref} className="box">
      <button className="close-icon" onClick={()=>props.setstate(false)}>X</button>
      <div className="popup-title">{props.message[0]}</div>
      <div className="popup-content">{props.message[1]}</div>
    </div>
  </div>
  )
}
 
export default Popup;