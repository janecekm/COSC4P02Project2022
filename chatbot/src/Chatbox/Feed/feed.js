import React, {useEffect, useState} from 'react';
import "./feed.css"
import ReactDOM from "react-dom";
import { useRef } from 'react';
import ClipButton from '../ClipButton/clipbutton';
class Message extends React.Component {
  render() {
    return (
      <div className={this.props.type}>{this.props.text}</div>
    );
  }
};

const Feed = () => {
  const [messagesList, setMessagesList] = useState([]);
  const[questions,setQuestions] = useState(null);
  const [reply, setReply] = useState(null);
  useEffect(()=>{
    const requestOption ={
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message:questions})
    };
    fetch("/",requestOption).then((response)=>{return response.json()}).then((data) => {setReply(data['message'])});
    console.log(reply);
  },[questions])
  const poseQuery = ()  => {
    
    
    var query = document.getElementById("inputField").value;
    console.log(query);
    
    if (query !== "") {
      setMessagesList( prevMessages =>
        prevMessages.concat(<Message key={messagesList.length} text = {query} type = "user_message"/>)
      );
        // sending query
        setQuestions(query);
        
        
      
        //done query
        console.log("heelo");

      setMessagesList( prevMessages =>
        prevMessages.concat(<Message key={messagesList.length} text = {reply} type = "response"/>)
      );
      clearInput();
      scrollDown();
      document.getElementById("inputField").style.setProperty('--size',40+"px");
    }
  };

  const scrollDown = () => {
  }

  const clearInput = () => {
    document.getElementById("inputField").value = '';
  }
  const handler = (event) => {
    if (event.key === "Enter") {
      poseQuery();
    }
    else{
      var temp = document.getElementById('inputField');
      temp.style.setProperty('--size',temp.scrollHeight-4+"px");
    }
  }

  return (
    <div>
      <ClipButton messages = {messagesList}/>
      <div className='feed'>
        <div>
          {messagesList}
        </div>
        <div className = "end" ></div>
      </div>
      <div className='inputarea' id='inputarena'>
        <button className="clearButton" onClick={clearInput}>Clear</button>
        <textarea className = "inputBar" onKeyUp={(e) => handler(e)} 
        id = "inputField" placeholder="Type a query here..." maxLength={250}
        autoComplete="off" />
        <button className="enterButton" onClick={poseQuery}>Enter</button>
      </div>
    </div>

  );
};

export default Feed;