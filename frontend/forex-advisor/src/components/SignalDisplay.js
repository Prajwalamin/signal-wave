import React, { useState } from "react";
import axios from "axios";
import "./signal.css"; // Assuming this contains your custom styles, like explanation-scroll

const SignalDisplay = () => {
  const [symbol, setSymbol] = useState(""); // User input for the forex pair (e.g., EURUSD)
  const [signalData, setSignalData] = useState(null); // Holds the signal data from the API
  const [loading, setLoading] = useState(false); // Loading state for API call
  const [error, setError] = useState(null); // Error state for handling errors

  // Function to convert user input to the required format (EUR_USD)
  const formatSymbol = (input) => {
    const upperCaseInput = input.toUpperCase(); // Convert to uppercase
    return upperCaseInput.slice(0, 3) + "_" + upperCaseInput.slice(3); // Insert underscore
  };

  // Function to fetch the signal and explanation from the backend
  const fetchSignalData = async () => {
    setLoading(true);
    setError(null);

    const formattedSymbol = formatSymbol(symbol);
    const requestBody = { symbol: formattedSymbol };

    try {
      const response = await axios.post(
        "http://localhost:8000/generate-explanation",
        requestBody
      );
      setSignalData(response.data); // Save the API response (signal and explanation) to state
    } catch (err) {
      setError(
        `Error fetching data for ${symbol.toUpperCase()}. Please check the symbol and try again.`
      );
    } finally {
      setLoading(false);
    }
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (symbol.trim()) {
      fetchSignalData();
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-8 bg-white shadow-lg rounded-lg border border-gray-200">
      <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">
        Signal Wave
      </h2>

      {/* Input form for entering forex symbol */}
      <form onSubmit={handleSubmit} className="space-y-4 opacity-75">
        <label
          htmlFor="symbolInput"
          className="block text-md font-semibold text-gray-700"
        >
          Enter Forex Pair (e.g., EURUSD)
        </label>
        <input
          id="symbolInput"
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())} // Ensure input is always uppercase
          placeholder="EUR_USD"
          className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-400"
          required
        />
        <button
          type="submit"
          className={`w-full py-3 font-semibold rounded-lg transition duration-300 ${
            loading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700 text-white"
          }`}
          disabled={loading}
        >
          {loading ? "Fetching..." : "Get Signal"}
        </button>
      </form>

      {/* Show loading spinner while fetching data */}
      {loading && (
        <div className="flex justify-center mt-6">
          <div className="animate-spin rounded-full h-10 w-10 border-t-4 border-blue-500"></div>
        </div>
      )}

      {/* Show error message if there's an error */}
      {error && (
        <div className="mt-6 text-red-600 text-center font-medium">{error}</div>
      )}

      {/* Show the result when data is fetched successfully */}
      {signalData && (
        <div className="mt-8 p-6 bg-gray-50 shadow-inner rounded-lg border border-gray-200">
          <h3 className="text-2xl font-semibold mb-4 text-gray-800">
            Signal for <span className="text-blue-600">{symbol}</span>
          </h3>
          <div className="mb-3">
            <strong>Signal:</strong>{" "}
            <span
              className={`font-bold text-lg ${
                signalData.signal === "Strong Buy"
                  ? "text-green-600"
                  : signalData.signal === "Moderate Buy"
                  ? "text-green-400"
                  : signalData.signal === "Strong Sell"
                  ? "text-red-600"
                  : signalData.signal === "Moderate Sell"
                  ? "text-red-400"
                  : "text-yellow-600"
              }`}
            >
              {signalData.signal}
            </span>
          </div>
          <div className="mb-3 text-gray-700">
            <strong>Current Price:</strong> {signalData.current_price}
          </div>
          <div className="mb-3 text-gray-700">
            <strong>RSI:</strong> {signalData.rsi}
          </div>
          <div className="mb-3 text-gray-700">
            <strong>50 Day Moving Average:</strong> {signalData.ema_50}
          </div>
          <div className="mt-4">
            <strong>Explanation:</strong>
            <div className="explanation-scroll p-3 mt-2 bg-white border border-gray-300 rounded-lg">
              {signalData.explanation}
            </div>

            {/* Disclaimer section */}
            <div className="fixed bottom-5 right-5 bg-yellow-100 border bg-opacity-50 border-gray-300 p-3 rounded-md text-xs text-gray-600 shadow-md w-40">
              <p>
                Disclaimer: This app provides educational information and is not
                intended for real financial advice. Use signals with caution.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SignalDisplay;
