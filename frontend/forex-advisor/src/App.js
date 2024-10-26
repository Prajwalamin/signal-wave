import React from "react";
import SignalDisplay from "./components/SignalDisplay"; // Import the SignalDisplay component

function App() {
  return (
    <div className="App">
      {/* Render the SignalDisplay component */}
      <SignalDisplay />{" "}
      {/* This is the main component that will handle the user input and display the signal */}
    </div>
  );
}

export default App;
