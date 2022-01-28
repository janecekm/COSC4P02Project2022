import React from 'react';
import ReactDOM from 'react-dom';
import Navbar from './Navbar/navbar';
import Chatbox from './Chatbox/chatbox'
import "./index.css";

ReactDOM.render(
  <>
  <Navbar />
  <Chatbox />
  
  <footer className='disclaimer'>this is not my fault</footer>
  </>
  ,
  document.getElementById('root'),

);
