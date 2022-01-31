import React, {useState} from 'react';
import "./feed.css"
import ReactDOM from "react-dom";

class Message extends React.Component {
  render() {
    return (
      <div>{this.props.text}</div>
    );
  }
};

const Feed = () => {
  const [inputList, setInputList] = useState([]);
  const onAddBtnClick = event => {
    var query = document.getElementById("inputField").value;
    if (query != "") {
      setInputList(inputList.concat(<Message key={inputList.length} text = {query} />));
      clearInput();
    }
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