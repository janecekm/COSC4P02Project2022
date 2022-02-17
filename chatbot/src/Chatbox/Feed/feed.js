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
  useEffect(()=>{
    document.getElementById("inputField").setAttribute("disable","true");
    const requestOption ={
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message:questions})
    };
    fetch("/",requestOption).then((response)=>{return response.json()}).then((data) => {
    console.log(data['message']);
    if(data['message']!=null)
    setMessagesList( prevMessages =>
      prevMessages.concat(<Message key={messagesList.length} text = {data['message']} type = "response"/>)
    );
  }
  );//triggers use effect for reply
  },[questions])

  const poseQuery =  async ()  => {
    var query = document.getElementById("inputField").value;
    console.log(query);
    
    if (query !== "") {
      setMessagesList( prevMessages =>
        prevMessages.concat(<Message key={messagesList.length} text = {query} type = "user_message"/>)
      );
        // sending query
        await setQuestions(query);//triggers useEffect for questions
        
        
      
        //done query
        console.log("query gotten");

     
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
        <textarea disabled={false} className = "inputBar" onKeyUp={(e) => handler(e)} 
        id = "inputField" placeholder="Type a query here..." maxLength={250}
        autoComplete="off" />
        <button className="enterButton" onClick={poseQuery}>Enter</button>
      </div>
    </div>

  );
};

export default Feed;
