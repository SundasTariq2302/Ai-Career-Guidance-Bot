import React from "react";

export default function MessageBubble({ sender, text }) {
  const isBot = sender === "Bot";
  return (
    <div className={`flex ${isBot ? "justify-start" : "justify-end"}`}>
      <div
        className={`p-3 max-w-[70%] rounded-2xl text-sm ${
          isBot
            ? "bg-gray-200 text-gray-800"
            : "bg-purple-600 text-white"
        }`}
      >
        <strong>{sender}:</strong> {text}
      </div>
    </div>
  );
}
