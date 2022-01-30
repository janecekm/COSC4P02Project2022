import React, {useState} from 'react';
import "./feed.css"
import ReactDOM from "react-dom";

const Message = () => {
  return (
    <div>Message</div>
  );
};

const Feed = () => {
  const [inputList, setInputList] = useState([]);
  const onAddBtnClick = event => {
    setInputList(inputList.concat(<Message key={inputList.length} />));
  };
  const clearInput = () => {
    document.getElementById("inputField").value = "";
  }
  
  return (
    <div>
      <div className='feed'>
        {inputList}
      </div>
      <button onClick={onAddBtnClick}>Enter</button>
      <input id = "inputField" placeholder="Type a query here..."></input>
      <button onClick={clearInput}>Clear</button>
    </div>
  );
};


export default Feed;