// src/App.js
import React, { useState } from "react";
import "./index.css";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [darkMode, setDarkMode] = useState(false);
  const [accentColor, setAccentColor] = useState("bg-green-500"); // Default accent color

  const sendMessage = async () => {
    if (!input.trim()) return;

    const updatedMessages = [...messages, { sender: "You", text: input }];
    setMessages(updatedMessages);

    try {
      const response = await fetch("http://127.0.0.1:8000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: "User",
          skills: input.split(" "),
          interests: [],
        }),
      });

      const data = await response.json();

      const botReply = data.recommendations
        ? data.recommendations
            .map(
              (rec) =>
                `${rec.career}: ${rec.description} | Next: ${rec.recommended_next_steps.join(", ")}`
            )
            .join("\n\n")
        : data.message || "No response";

      setMessages([...updatedMessages, { sender: "Bot", text: botReply }]);
    } catch (error) {
      setMessages([
        ...updatedMessages,
        { sender: "Bot", text: "Error: Could not connect to backend." },
      ]);
    }

    setInput("");
  };

  return (
    <div className={`${darkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-black"} min-h-screen grid grid-cols-12`}>
      
      {/* Sidebar */}
      <div className="col-span-2 bg-purple-600 text-white flex flex-col items-center py-6 space-y-8">
        <div className="text-xl font-bold">CareerBot</div>

        <div className="space-y-6 text-sm">
          <div className="hover:text-purple-300 cursor-pointer">Home</div>
          <div className="hover:text-purple-300 cursor-pointer">Settings</div>
          <div className="hover:text-purple-300 cursor-pointer">Chat</div>
        </div>

        {/* Theme Switch */}
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="mt-8 bg-white text-purple-600 px-3 py-1 rounded hover:bg-purple-200 text-sm"
        >
          {darkMode ? "Light Mode" : "Dark Mode"}
        </button>

        {/* Accent Color Selector */}
        <div className="mt-8 space-x-2">
          {["bg-green-500", "bg-blue-500", "bg-pink-500", "bg-yellow-500"].map((color) => (
            <button
              key={color}
              onClick={() => setAccentColor(color)}
              className={`${color} w-6 h-6 rounded-full hover:scale-110 transform`}
              title={`Set ${color}`}
            />
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="col-span-10 p-8">
        <h1 className="text-3xl font-bold mb-6">AI Career Guidance Chatbot</h1>

        <div className={`${darkMode ? "bg-gray-800" : "bg-white"} rounded-xl p-6 shadow-md flex flex-col justify-between min-h-[500px]`}>
          
          {/* Chat Messages */}
          <div className="overflow-y-auto mb-4 space-y-3">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`max-w-[75%] px-4 py-2 rounded-xl ${
                  msg.sender === "Bot"
                    ? darkMode
                      ? "bg-gray-600 text-white"
                      : "bg-gray-200 text-black"
                    : `${accentColor} text-white self-end ml-auto`
                }`}
              >
                <strong>{msg.sender}: </strong> {msg.text}
              </div>
            ))}
          </div>

          {/* Input */}
          <div className="mt-4 flex">
            <input
              type="text"
              placeholder="Type your skills & interests..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              className="p-2 rounded-l-md border border-gray-300 w-full text-black"
            />
            <button
              onClick={sendMessage}
              className={`${accentColor} text-white px-4 py-2 rounded-r-md hover:opacity-90`}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
