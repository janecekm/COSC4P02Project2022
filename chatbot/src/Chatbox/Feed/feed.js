import React, {forwardRef, useEffect, useState} from 'react';
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

  const [messagesList, setMessagesList] = useState([<Message key={0} text = {func("message")} type = "response"/>]);//holds the messages between user and the chat bot
  const[questions,setQuestions] = useState(null);// holds the question asked by the user
  useEffect(()=>{
    if (questions != null){//if a question is asked
    document.getElementById("think").style.setProperty("display", "flex");//set the display to thinking
    scrollDown(document.getElementById("feed"))
    document.getElementById("inputField").contentEditable = false;//make the text box not editable
    document.getElementById("inputField").style.setProperty("caret-color", "transparent");
    const requestOption ={
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message:questions})
    };//building the request with the question
    var url = window.location.href.toString();
    var isCanada = url.search("/canada");
    
    var sendToUrl = isCanada==-1?"/brock":"/canada"//checks and finds which url we are in.

    fetch(sendToUrl,requestOption).then((response)=>{return response.json()}).then((data) => {
      console.log(data);
      document.getElementById("inputField").contentEditable = true;//editable after the data is processed.
      document.getElementById("think").style.setProperty("display", "none");
      setMessagesList( prevMessages =>
        prevMessages.concat(<Message key={messagesList.length} text = {data['message']} type = "response"/>)
      );//adds the messages to the message list
      scrollDown(document.getElementById("feed"));
      document.getElementById("inputField").focus();
      document.getElementById("inputField").style.setProperty("caret-color", "black");
    }
  );//triggers use effect for reply

  };},[questions])//the trigger happens when there is a change of questions

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
    else if (query === "\n\n\n") {
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
        <div className="clearButton" onClick={clearInput}>{func("clear")}</div>
              <span onKeyDown={(e) => limiter(e)} onKeyUp={(e) => handler(e)} id = "inputField" 
              className='inputBar' role="textbox" 
              contentEditable ='true' data-placeholder={func('inputmessage')}>
              </span>
        <div className="enterButton" onClick={poseQuery}>{func("enter")}</div>
      </div>
    </div>

  );
};

export default Feed;
