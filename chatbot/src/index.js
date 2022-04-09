import React from 'react';
import ReactDOM from 'react-dom';
import Navbar from './Navbar/navbar';
import Chatbox from './Chatbox/chatbox'
import "./index.css";
import langprocess from "./Language/Lanprocess"

(async()=>{
  var url = window.location.href.toString();
  var isCanada = url.search("/canada");
  if(isCanada===-1)//if we are in the /Brock domain
    await import("./brockcolor.css");
  else
    await import("./canadacolor.css");
})();

window.addEventListener("offline",(Event)=>{//if the user is online
  document.getElementById("inputField").contentEditable = false;
})

window.addEventListener("online",(Event)=>{//if the user is online
  document.getElementById("inputField").contentEditable = true;
})

ReactDOM.render(
  <>
  <Navbar />
  <Chatbox />
  <footer className='disclaimer'>{langprocess("disclaimer")}</footer>
  </>
  ,
  document.getElementById('root'),

);
