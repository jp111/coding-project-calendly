import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
import unittest
from calendly_api.services.availability_service import AvailabilityService
from calendly_api.database.mongo_client import mongodb_client

class TestAvailabilityService(unittest.TestCase):
    def setUp(self):
        """Set up the test environment before each test."""
        self.service = AvailabilityService()
        self.service.collection.delete_many({})  # Clear the collection before each test

    def test_initialize_user(self):
        """Test if a new user is initialized correctly with all time slots unavailable."""
        self.service.initialize_user("user1")
        user_data = self.service.collection.find_one({"user_id": "user1"})
        self.assertIsNotNone(user_data)
        self.assertEqual(len(user_data["availability"]), 48)
        self.assertFalse(any(user_data["availability"]))

    def test_set_availability(self):
        """Test setting availability for specific time slots."""
        self.service.set_availability("user1", "09:00", "10:00", True)
        user_data = self.service.collection.find_one({"user_id": "user1"})
        self.assertTrue(user_data["availability"][18])
        self.assertTrue(user_data["availability"][19])
        
        self.service.set_availability("user1", "09:00", "10:00", False)
        user_data = self.service.collection.find_one({"user_id": "user1"})
        self.assertFalse(user_data["availability"][18])
        self.assertFalse(user_data["availability"][19])

    def test_update_availability(self):
        """Test updating availability for multiple time slots."""
        updates = [("09:00", "10:00", True), ("11:00", "12:00", True)]
        self.service.update_availability("user1", updates)
        user_data = self.service.collection.find_one({"user_id": "user1"})
        self.assertTrue(user_data["availability"][18])
        self.assertTrue(user_data["availability"][19])
        self.assertTrue(user_data["availability"][22])
        self.assertTrue(user_data["availability"][23])

    def test_is_available(self):
        """Test checking if a user is available at a specific time."""
        self.service.set_availability("user1", "09:00", "10:00", True)
        self.assertTrue(self.service.is_available("user1", "09:30"))
        self.assertFalse(self.service.is_available("user1", "10:30"))

    def test_find_availability(self):
        """Test finding all available slots within a given time range."""
        self.service.set_availability("user1", "09:00", "10:00", True)
        available_slots = self.service.find_availability("user1", "08:00", "11:00")
        self.assertEqual(available_slots, ['09:00-09:30', '09:30-10:00'])

    def test_find_overlap(self):
        """Test finding overlapping available slots between two users."""
        self.service.set_availability("user1", "09:00", "10:00", True)
        self.service.set_availability("user2", "09:30", "10:30", True)
        overlaps = self.service.find_overlap("user1", "user2")
        self.assertEqual(overlaps, ['09:30-10:00'])

    def test_edge_cases(self):
        """Test various edge cases for the availability service."""
        # User not initialized
        self.assertFalse(self.service.is_available("new_user", "12:00"))

        # Invalid time format
        with self.assertRaises(ValueError):
            self.service.set_availability("user1", "invalid_time", "12:00", True)
        
        with self.assertRaises(ValueError):
            self.service.update_availability("user1", [("invalid_time", "12:00", True)])

        # Time outside of range
        with self.assertRaises(ValueError):
            self.service.set_availability("user1", "24:00", "25:00", True)

        with self.assertRaises(ValueError):
            self.service.update_availability("user1", [("24:00", "25:00", True)])

if __name__ == '__main__':
    unittest.main()
