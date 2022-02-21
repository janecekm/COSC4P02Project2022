import React from 'react';
import ReactDOM from 'react-dom';
import Navbar from './Navbar/navbar';
import Chatbox from './Chatbox/chatbox'
import "./index.css";
import langprocess from "./Language/Lanprocess"

      

ReactDOM.render(
  <>
  <Navbar />
  <Chatbox />
  
  <footer className='disclaimer'>{langprocess("disclaimer")}</footer>
  </>
  ,
  document.getElementById('root'),

);
