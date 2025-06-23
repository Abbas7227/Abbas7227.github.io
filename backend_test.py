#!/usr/bin/env python3
import requests
import json
import unittest
import sys

# Get the backend URL from the frontend/.env file
BACKEND_URL = "https://8dbf5533-e009-4e72-b85f-8271a1c8c578.preview.emergentagent.com"
API_URL = f"{BACKEND_URL}/api"

class FootballPlayRecommendationTest(unittest.TestCase):
    def setUp(self):
        self.recommend_play_url = f"{API_URL}/recommend-play"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def test_api_root(self):
        """Test the API root endpoint"""
        response = requests.get(f"{API_URL}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Football Play Recommendation System API")
    
    def test_red_zone_scenario(self):
        """Test red zone scenario: yard_position=85, down='4th', yard_gain='medium'"""
        payload = {
            "yard_position": 85,
            "down": "4th",
            "yard_gain": "medium"
        }
        response = requests.post(self.recommend_play_url, headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify response structure
        self.assertIn("recommended_plays", data)
        self.assertIn("field_situation", data)
        self.assertIn("strategy_note", data)
        
        # Verify specific play recommendation
        self.assertIn("Slot Fade", data["recommended_plays"])
        self.assertEqual(data["field_situation"], "Red Zone - Score Now")
        self.assertEqual(data["strategy_note"], "All or nothing - go for it!")
    
    def test_own_territory_scenario(self):
        """Test own territory: yard_position=10, down='1st', yard_gain='long'"""
        payload = {
            "yard_position": 10,
            "down": "1st",
            "yard_gain": "long"
        }
        response = requests.post(self.recommend_play_url, headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify response structure
        self.assertIn("recommended_plays", data)
        self.assertIn("field_situation", data)
        self.assertIn("strategy_note", data)
        
        # Verify specific play recommendation
        self.assertIn("Post Wheel", data["recommended_plays"])
        self.assertEqual(data["field_situation"], "Own Territory - Conservative")
        self.assertEqual(data["strategy_note"], "Establish rhythm and set up future downs")
    
    def test_midfield_scenario(self):
        """Test midfield: yard_position=50, down='2nd', yard_gain='medium'"""
        payload = {
            "yard_position": 50,
            "down": "2nd",
            "yard_gain": "medium"
        }
        response = requests.post(self.recommend_play_url, headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify response structure
        self.assertIn("recommended_plays", data)
        self.assertIn("field_situation", data)
        self.assertIn("strategy_note", data)
        
        # Verify field situation and strategy note
        self.assertEqual(data["field_situation"], "Midfield - Balanced")
        self.assertEqual(data["strategy_note"], "Keep the chains moving")
    
    def test_edge_case_scenario(self):
        """Test edge case: yard_position=100, down='3rd', yard_gain='medium'"""
        payload = {
            "yard_position": 100,
            "down": "3rd",
            "yard_gain": "medium"
        }
        response = requests.post(self.recommend_play_url, headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify response structure
        self.assertIn("recommended_plays", data)
        self.assertIn("field_situation", data)
        self.assertIn("strategy_note", data)
        
        # Verify specific play recommendation
        self.assertIn("Switch Verticals", data["recommended_plays"])
        self.assertEqual(data["field_situation"], "Red Zone - Score Now")
        self.assertEqual(data["strategy_note"], "Must convert to keep the drive alive")
    
    def test_invalid_yard_position(self):
        """Test invalid yard position (outside 0-100 range)"""
        # Test negative yard position
        payload = {
            "yard_position": -10,
            "down": "1st",
            "yard_gain": "medium"
        }
        response = requests.post(self.recommend_play_url, headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 422)  # Validation error
        
        # Test yard position > 100
        payload = {
            "yard_position": 110,
            "down": "1st",
            "yard_gain": "medium"
        }
        response = requests.post(self.recommend_play_url, headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_invalid_down(self):
        """Test invalid down value"""
        payload = {
            "yard_position": 50,
            "down": "5th",  # Invalid down
            "yard_gain": "medium"
        }
        response = requests.post(self.recommend_play_url, headers=self.headers, json=payload)
        # The API doesn't validate down values, so it should still return 200
        # but we can check that it returns a valid response structure
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("recommended_plays", data)
        self.assertIn("field_situation", data)
        self.assertIn("strategy_note", data)
    
    def test_invalid_yard_gain(self):
        """Test invalid yard gain value"""
        payload = {
            "yard_position": 50,
            "down": "2nd",
            "yard_gain": "invalid"  # Invalid yard gain
        }
        response = requests.post(self.recommend_play_url, headers=self.headers, json=payload)
        # The API doesn't validate yard_gain values, so it should still return 200
        # but we can check that it returns a valid response structure
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("recommended_plays", data)
        self.assertIn("field_situation", data)
        self.assertIn("strategy_note", data)
    
    def test_missing_parameters(self):
        """Test missing required parameters"""
        # Missing yard_position
        payload = {
            "down": "1st",
            "yard_gain": "medium"
        }
        response = requests.post(self.recommend_play_url, headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 422)  # Validation error
        
        # Missing down
        payload = {
            "yard_position": 50,
            "yard_gain": "medium"
        }
        response = requests.post(self.recommend_play_url, headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 422)  # Validation error
        
        # Missing yard_gain
        payload = {
            "yard_position": 50,
            "down": "1st"
        }
        response = requests.post(self.recommend_play_url, headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_cors_functionality(self):
        """Test CORS functionality by checking if API is accessible from different origins"""
        payload = {
            "yard_position": 50,
            "down": "2nd",
            "yard_gain": "medium"
        }
        # Add an Origin header to simulate a cross-origin request
        headers = self.headers.copy()
        headers["Origin"] = "http://example.com"
        
        response = requests.post(self.recommend_play_url, headers=headers, json=payload)
        self.assertEqual(response.status_code, 200)
        
        # The API should still return a valid response even with a different origin
        data = response.json()
        self.assertIn("recommended_plays", data)
        self.assertIn("field_situation", data)
        self.assertIn("strategy_note", data)

if __name__ == "__main__":
    # Run the tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)