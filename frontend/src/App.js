import React, { useState } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [yardPosition, setYardPosition] = useState(50);
  const [down, setDown] = useState("1st");
  const [yardGain, setYardGain] = useState("medium");
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getRecommendations = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API}/recommend-play`, {
        yard_position: yardPosition,
        down: down,
        yard_gain: yardGain
      });
      
      setRecommendations(response.data);
    } catch (err) {
      console.error('Error getting recommendations:', err);
      setError('Failed to get play recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getFieldZoneColor = (yard) => {
    if (yard <= 20) return "bg-red-100 border-red-300";
    if (yard <= 50) return "bg-yellow-100 border-yellow-300";
    if (yard <= 80) return "bg-green-100 border-green-300";
    return "bg-blue-100 border-blue-300";
  };

  const getFieldZoneText = (yard) => {
    if (yard <= 20) return "Own Territory";
    if (yard <= 50) return "Midfield";
    if (yard <= 80) return "Red Zone Approach";
    return "Red Zone";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            🏈 Football Play Caller
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Get strategic play recommendations based on your field position, down, and situation
          </p>
        </div>

        <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-8">
          {/* Input Panel */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span className="mr-3">⚙️</span>
              Game Situation
            </h2>
            
            {/* Yard Position */}
            <div className="mb-8">
              <label className="block text-lg font-semibold text-gray-700 mb-3">
                Field Position: {yardPosition} yard line
              </label>
              <div className={`p-4 rounded-lg border-2 ${getFieldZoneColor(yardPosition)} mb-4`}>
                <div className="text-center font-semibold text-gray-700">
                  {getFieldZoneText(yardPosition)}
                </div>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={yardPosition}
                onChange={(e) => setYardPosition(parseInt(e.target.value))}
                className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              />
              <div className="flex justify-between text-sm text-gray-500 mt-2">
                <span>Own End Zone (0)</span>
                <span>Opponent End Zone (100)</span>
              </div>
            </div>

            {/* Down Selection */}
            <div className="mb-8">
              <label className="block text-lg font-semibold text-gray-700 mb-3">
                Down
              </label>
              <div className="grid grid-cols-4 gap-2">
                {['1st', '2nd', '3rd', '4th'].map((d) => (
                  <button
                    key={d}
                    onClick={() => setDown(d)}
                    className={`py-3 px-4 rounded-lg font-semibold transition-all ${
                      down === d
                        ? 'bg-blue-600 text-white shadow-lg transform scale-105'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {d}
                  </button>
                ))}
              </div>
            </div>

            {/* Yard Gain Target */}
            <div className="mb-8">
              <label className="block text-lg font-semibold text-gray-700 mb-3">
                Target Yardage
              </label>
              <div className="space-y-2">
                {[
                  { value: 'short', label: 'Short (0-30 yards)', color: 'bg-green-500' },
                  { value: 'medium', label: 'Medium (30-60 yards)', color: 'bg-yellow-500' },
                  { value: 'long', label: 'Long (60-90 yards)', color: 'bg-red-500' }
                ].map((option) => (
                  <button
                    key={option.value}
                    onClick={() => setYardGain(option.value)}
                    className={`w-full py-3 px-4 rounded-lg font-semibold transition-all flex items-center ${
                      yardGain === option.value
                        ? 'bg-blue-600 text-white shadow-lg transform scale-105'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    <div className={`w-4 h-4 rounded-full ${option.color} mr-3`}></div>
                    {option.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Get Recommendations Button */}
            <button
              onClick={getRecommendations}
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-6 rounded-xl font-bold text-lg hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-2"></div>
                  Analyzing...
                </div>
              ) : (
                '🎯 Get Play Recommendations'
              )}
            </button>
          </div>

          {/* Results Panel */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span className="mr-3">📋</span>
              Recommended Plays
            </h2>

            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
                {error}
              </div>
            )}

            {!recommendations && !error && (
              <div className="text-center py-12 text-gray-500">
                <div className="text-6xl mb-4">🏈</div>
                <p className="text-lg">
                  Set your game situation and click "Get Play Recommendations" to see strategic options
                </p>
              </div>
            )}

            {recommendations && (
              <div className="space-y-6">
                {/* Field Situation */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-700 mb-2">Field Situation</h3>
                  <p className="text-gray-600">{recommendations.field_situation}</p>
                </div>

                {/* Strategy Note */}
                <div className="bg-blue-50 rounded-lg p-4">
                  <h3 className="font-semibold text-blue-700 mb-2">Strategy</h3>
                  <p className="text-blue-600">{recommendations.strategy_note}</p>
                </div>

                {/* Recommended Plays */}
                <div>
                  <h3 className="font-semibold text-gray-700 mb-4">Recommended Plays</h3>
                  <div className="space-y-3">
                    {recommendations.recommended_plays.map((play, index) => (
                      <div
                        key={index}
                        className="bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg p-4 flex items-center"
                      >
                        <div className="bg-green-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold mr-4">
                          {index + 1}
                        </div>
                        <span className="font-semibold text-gray-800">{play}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Quick Stats */}
                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-700 mb-2">Quick Stats</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-600">{yardPosition}</div>
                      <div className="text-sm text-gray-500">Yard Line</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-600">{down}</div>
                      <div className="text-sm text-gray-500">Down</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-600">{yardGain}</div>
                      <div className="text-sm text-gray-500">Target</div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500">
          <p>📊 Professional Football Play Recommendation System</p>
        </div>
      </div>
    </div>
  );
}

export default App;