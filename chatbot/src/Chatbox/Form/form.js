import React, {useState} from 'react';
import "./form.css"

function Form (){
    const [open, setopen] = useState(false);
    return (
        <form className="form">
            <input
                    className="input"
                    type="text"
                    placeholder="Type a query here..."

                    /*value={message}
                    
                    onChange={({ target: { value } }) => setMessage(value)}
                    onKeyPress={event => event.key === 'Enter' ? sendMessage(event) : null}
                    <button className="sendButton" onClick={e => sendMessage(e)}>Send</button>
                    */
                />
            
            
        </form>
    )
}
export default Form;