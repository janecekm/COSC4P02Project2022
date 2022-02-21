import React from 'react';
import ReactDOM from 'react-dom';
import Navbar from './Navbar/navbar';
import Chatbox from './Chatbox/chatbox'
import "./index.css";

ReactDOM.render(
  
  <>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
  <Navbar />
  <Chatbox />
  <footer className='disclaimer'>All information taken from Brock University</footer>
  </>
  ,
  document.getElementById('root'),

);
