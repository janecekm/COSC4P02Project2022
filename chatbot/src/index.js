import React from 'react';
import ReactDOM from 'react-dom';
import Navbar from './Navbar/navbar';
import Chatbox from './Chatbox/chatbox'
import "./index.css";
import langprocess from "./Language/Lanprocess"

// return v==-1?values[document.documentElement.lang][name]:val[document.documentElement.lang][name];
(async()=>{
  var temp = window.location.href.toString();
  var v = temp.search("/canada");
  if(v===-1)
    await import("./brockcolor.css");
  else
    await import("./canadacolor.css");
})();

ReactDOM.render(
  
  <>
  <Navbar />
  <Chatbox />
  <footer className='disclaimer'>{langprocess("disclaimer")}</footer>
  </>
  ,
  document.getElementById('root'),

);
