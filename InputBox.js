import React, { useState } from 'react';

function InputBox() {
  const [inputValue, setInputValue] = useState('');
  const [responseMessage, setResponseMessage] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSendClick = async () => {
    if (inputValue.trim()) {
      try {
        const response = await fetch("http://localhost:8000/send-message/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ message: inputValue })
        });

        const data = await response.json();
        if (response.ok) {
          setResponseMessage(data.response);
        } else {
          setResponseMessage(data.detail || "Error sending message");
        }
      } catch (error) {
        setResponseMessage("Error: Unable to send message");
      }

      setInputValue(''); // Clear the input after submission
    }
  };

  return (
    <div className="input-container">
      <input
        type="text"
        placeholder="Type your message..."
        value={inputValue}
        onChange={handleInputChange}
        className="input-box"
      />
      <button onClick={handleSendClick} className="send-button">Send</button>

      {/* Display response from FastAPI */}
      {responseMessage && <p>{responseMessage}</p>}
    </div>
  );
}

export default InputBox;