import React, {useEffect, useState} from 'react';
import "./feed.css"
import ReactDOM from "react-dom";
import { useRef } from 'react';

class Message extends React.Component {
  render() {
    return (
      <div className={this.props.type}>{this.props.text}</div>
    );
  }
};

const Feed = () => {
  const [messagesList, setMessagesList] = useState([]);
  const poseQuery = ()  => {
    var query = document.getElementById("inputField").value;
    if (query !== "") {
      setMessagesList( prevMessages =>
        prevMessages.concat(<Message key={messagesList.length} text = {query} type = "user_message"/>)
      );
      setMessagesList( prevMessages =>
        prevMessages.concat(<Message key={messagesList.length} text = "Generic Response" type = "response"/>)
      );
      clearInput();
      scrollDown();
    }
  };

  const scrollDown = () => {
  }


  const clearInput = () => {
    document.getElementById("inputField").value = "";
  }
  const handler = (event) => {
    if (event.key === "Enter") {
      poseQuery();
    }
  }


  return (
    <div>
      <div className='feed'>
        <div>
          {messagesList}
        </div>
        <div className = "end" ></div>
      </div>
      <div>
        <button className="clearButton" onClick={clearInput}>Clear</button>
        <input className = "inputBar" onKeyPress={(e) => handler(e)} 
        id = "inputField" placeholder="Type a query here..." maxLength={250}></input>
        <button className="enterButton" onClick={poseQuery}>Enter</button>
      </div>
    </div>

  );
};


export default Feed;
