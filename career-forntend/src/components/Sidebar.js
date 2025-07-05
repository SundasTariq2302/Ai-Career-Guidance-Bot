import React from "react";

export default function Sidebar() {
  return (
    <div className="col-span-2 bg-purple-700 text-white flex flex-col items-center py-6 space-y-8">
      <div className="text-3xl font-bold">🤖</div>
      <div className="space-y-8 text-xl">
        <div className="hover:text-purple-300 cursor-pointer">🏠</div>
        <div className="hover:text-purple-300 cursor-pointer">⚙️</div>
        <div className="hover:text-purple-300 cursor-pointer">💬</div>
      </div>
    </div>
  );
}
