import React, { useState } from 'react';
import axios from 'axios';

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');

  const sendMessage = async () => {
    const newMessages = [...messages, { sender: 'user', text: userInput }];
    setMessages(newMessages);

    // API call to FastAPI /recommend
    try {
        const response = await axios.post('http://localhost:8000/recommend', {
        name: "Sundas",
        skills: userInput.split(" "),
        interests: userInput.split(" ")
      });

      const recs = response.data.recommendations || [];
      const botMessage = recs.length
        ? recs.map(r => `${r.career}: ${r.description} | Next: ${r.recommended_next_steps.join(", ")}`).join("\n\n")
        : response.data.message;

      setMessages([...newMessages, { sender: 'bot', text: botMessage }]);
    } catch (error) {
      setMessages([...newMessages, { sender: 'bot', text: 'Error: Could not connect to backend.' }]);
    }

    setUserInput('');
  };
return (
  <div className="max-w-xl mx-auto p-4">
    <div className="bg-white rounded shadow p-4 h-96 overflow-y-auto mb-4">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`my-2 ${msg.sender === 'user' ? 'text-right' : 'text-left'}`}
        >
          <span className="font-semibold">{msg.sender === 'user' ? 'You' : 'Bot'}:</span> {msg.text}
        </div>
      ))}
    </div>
    <div className="flex">
      <input
        type="text"
        className="border p-2 flex-grow rounded-l"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="Type your skills & interests..."
      />
      <button
        onClick={sendMessage}
        className="bg-blue-500 text-white px-4 rounded-r hover:bg-blue-600"
      >
        Send
      </button>
    </div>
  </div>
);
}

export default Chatbot;
