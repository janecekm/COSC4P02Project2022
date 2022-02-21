import React from 'react';
import ReactDOM from 'react-dom';
import Navbar from './Navbar/navbar';
import Chatbox from './Chatbox/chatbox'
import "./index.css";
import langprocess from "./Language/Lanprocess"


var temp = window.location.href.toString();
var v = temp.search("/canada");
if(v<0){//in canada
  var t = document.getElementById('root');
  t.style.setProperty('--primary-color',getComputedStyle(t).getPropertyValue('--brock-colors'));
  t.style.setProperty('--secondary-color',getComputedStyle(t).getPropertyValue('--brock-secondary-colors'))
}
else{//brock
  var t = document.getElementById('root');
  t.style.setProperty('--primary-color',getComputedStyle(t).getPropertyValue('--canada-colors'));
  t.style.setProperty('--secondary-color',getComputedStyle(t).getPropertyValue('--canada-secondary-colors'))
  
}


ReactDOM.render(
  <>
  <Navbar />
  <Chatbox />
  
  <footer className='disclaimer'>{langprocess("disclaimer")}</footer>
  </>
  ,
  document.getElementById('root'),

);
