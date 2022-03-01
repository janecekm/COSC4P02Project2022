import React, {useEffect, useState} from 'react';
import "./feed.css"
import ClipButton from '../ClipButton/clipbutton';
import Thinking from '../Thinking/thinking';
import func from "../../Language/Lanprocess";

class Message extends React.Component {
  render() {
    return (
      <div className={this.props.type}>{this.props.text}</div>
    );
  }
};

const Feed = () => {

  const [messagesList, setMessagesList] = useState([<Message key={0} text = {func("message")} type = "response"/>]);
  const[questions,setQuestions] = useState(null);
  useEffect(()=>{
    if (questions != null){
    document.getElementById("think").style.setProperty("display", "flex");
    scrollDown(document.getElementById("feed"))
    document.getElementById("inputField").contentEditable = false;
    document.getElementById("inputField").style.setProperty("caret-color", "transparent");
    const requestOption ={
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message:questions})
    };
    fetch("/brock",requestOption).then((response)=>{return response.json()}).then((data) => {
      console.log(data['message']);
      document.getElementById("inputField").contentEditable = true;
      
      document.getElementById("think").style.setProperty("display", "none");
      setMessagesList( prevMessages =>
        prevMessages.concat(<Message key={messagesList.length} text = {data['message']} type = "response"/>)
      );
      scrollDown(document.getElementById("feed"));
      document.getElementById("inputField").focus();
      document.getElementById("inputField").style.setProperty("caret-color", "black");
    }
    
  
  );//triggers use effect for reply

  };},[questions])

  const poseQuery =  async ()  => {
    var query = document.getElementById("inputField").innerText;
    console.log(query);
    
    if (query !== "" & query !== "\n\n\n") {
      console.log(query);
      setMessagesList( prevMessages =>
        prevMessages.concat(<Message key={messagesList.length} text = {query} type = "user_message"/>)
      );
      scrollDown(document.getElementById("feed"));
      // sending query
      await setQuestions(query);//triggers useEffect for questions
      //done query
      console.log("query gotten");

      setQuestions(null);
      clearInput();
    }
    else if (query == "\n\n\n") {
      clearInput();
    }
  };

  const scrollDown = (node) => {
    node.scrollTop = node.scrollHeight;
  }

  const clearInput = () => {
    document.getElementById("inputField").innerText = '';
  }

  const handler = (event) => {
    if (event.key === "Enter") {
      poseQuery();
    }
  }

  const limiter = (event) => {
    if (event.key !== "Backspace" & event.key !== "Enter" 
    & document.getElementById("inputField").innerText.length > 250) {
      event.preventDefault();
      console.log("input max reached");
    }
  }

  return (
    <div>
      <ClipButton messages = {messagesList}/> 
      <div className='feed' id = "feed">
        <div>
          {messagesList}
          <Thinking/>
        </div>
      </div>
      <div className="userTools">
        <button className="clearButton" onClick={clearInput}>{func("clear")}</button>
              <span onKeyDown={(e) => limiter(e)} onKeyUp={(e) => handler(e)} id = "inputField" 
              className='inputBar' role="textbox" 
              contentEditable ='true' data-placeholder={func('inputmessage')}>
              </span>
        <button className="enterButton" onClick={poseQuery}>{func("enter")}</button>
      </div>
    </div>

  );
};

export default Feed;
