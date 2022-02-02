import React, {useState} from 'react';
import "./feed.css"
import ReactDOM from "react-dom";

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
    if (query != "") {
      setMessagesList(
        messagesList.concat(<Message key={messagesList.length} text = {query} type = "user_message"/>)
      );
      clearInput();
    }
  };


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
        {messagesList}
      </div>
      <button className="clearButton" onClick={clearInput}>Clear</button>
      <input className = "inputBar" onKeyPress={(e) => handler(e)} id = "inputField" placeholder="Type a query here..."></input>
      <button className="enterButton" onClick={poseQuery}>Enter</button>
    </div>

  );
};


export default Feed;