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
    document.getElementById("inputField").disabled = true;
    document.getElementById("inputField").style.setProperty("caret-color", "transparent");
    const requestOption ={
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message:questions})
    };
    fetch("/brock",requestOption).then((response)=>{return response.json()}).then((data) => {
      console.log(data['message']);

      document.getElementById("inputField").disabled = false;
      
      document.getElementById("think").style.setProperty("display", "none");
      setMessagesList( prevMessages =>
        prevMessages.concat(<Message key={messagesList.length} text = {data['message']} type = "response"/>)
      );
      scrollDown(document.getElementById("feed"));
      document.getElementById("inputField").select();
      document.getElementById("inputField").style.setProperty("caret-color", "auto");
    }
    
  
  );//triggers use effect for reply

  };},[questions])

  const poseQuery =  async ()  => {
    var query = document.getElementById("inputField").value;
    console.log(query);
    
    if (query !== "" & query == "\n") {
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
      document.getElementById("inputField").style.setProperty('--size',40+"px");
    }
    else if (query == "\n") {
      clearInput();
    }
  };

  const scrollDown = (node) => {
    node.scrollTop = node.scrollHeight;
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
      <div className='feed' id = "feed">
        <div>
          {messagesList}
          <Thinking/>
        </div>
        
        
      </div>
      <div className='inputarea' id='inputarena'>
        <button className="clearButton" onClick={clearInput}>{func("clear")}</button>
        <textarea disabled = {false} className = "inputBar" onKeyUp={(e) => handler(e)} 
        id = "inputField" placeholder={func("inputmessage")} maxLength={250}
        autoComplete="off" />
        <button className="enterButton" onClick={poseQuery}>{func("enter")}</button>
      </div>
    </div>

  );
};

export default Feed;
