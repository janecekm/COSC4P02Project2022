import React, {forwardRef, useEffect, useState} from 'react';
import "./feed.css"
import ClipButton from '../ClipButton/clipbutton';
import Thinking from '../Thinking/thinking';
import func from "../../Language/Lanprocess";
import Zoomin from '../Zoomin/zoomin';
import Zoomout from '../Zoomout/zoomout'

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
    query = query.trim();
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
    else {
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
    <>
      <div className='feed' id = "feed">
      <ul className='contextmenu'>
      <li>
         <Zoomin />
        </li>
        <li>
          <Zoomout />
        </li>
        <li>
        <ClipButton messages = {messagesList}/> 
        </li>
        
      </ul>
        <div>
          {messagesList}
          <Thinking/>
        </div>
      </div>
      <div className="userTools">
        <div className="clearButton" onClick={clearInput}>
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-eraser" viewBox="0 0 16 16">
            <path d="M8.086 2.207a2 2 0 0 1 2.828 0l3.879 3.879a2 2 0 0 1 0 2.828l-5.5 5.5A2 2 0 0 1 7.879 15H5.12a2 2 0 0 1-1.414-.586l-2.5-2.5a2 2 0 0 1 0-2.828l6.879-6.879zm2.121.707a1 1 0 0 0-1.414 0L4.16 7.547l5.293 5.293 4.633-4.633a1 1 0 0 0 0-1.414l-3.879-3.879zM8.746 13.547 3.453 8.254 1.914 9.793a1 1 0 0 0 0 1.414l2.5 2.5a1 1 0 0 0 .707.293H7.88a1 1 0 0 0 .707-.293l.16-.16z"/>
          </svg>
        </div>
              <span onKeyDown={(e) => limiter(e)} onKeyUp={(e) => handler(e)} id = "inputField" 
              className='inputBar' role="textbox" 
              contentEditable ='true' data-placeholder={func('inputmessage')}>
              </span>
        <div className="enterButton" onClick={poseQuery}>
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
             <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576 6.636 10.07Zm6.787-8.201L1.591 6.602l4.339 2.76 7.494-7.493Z"/>
          </svg>
        </div>
      </div>
    </>

  );
};

export default Feed;
