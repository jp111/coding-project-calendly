import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 

from pymongo import MongoClient
from calendly_api.config.settings import MONGO_URI

class AvailabilityService:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client['calendly']
        self.collection = self.db['availability']

    def initialize_user(self, user_id):
        """Initialize a new user with all time slots unavailable."""
        if not self.collection.find_one({"user_id": user_id}):
            availability = [False] * 48
            self.collection.insert_one({"user_id": user_id, "availability": availability})

    def set_availability(self, user_id, start_time, end_time, available):
        """Set availability for specific time slots."""
        self.initialize_user(user_id)
        start_index = self._time_to_index(start_time)
        end_index = self._time_to_index(end_time)
        self.collection.update_one(
            {"user_id": user_id},
            {"$set": {f"availability.{i}": available for i in range(start_index, end_index)}}
        )

    def update_availability(self, user_id, updates):
        """Update availability for multiple time slots."""
        self.initialize_user(user_id)
        for start_time, end_time, available in updates:
            start_index = self._time_to_index(start_time)
            end_index = self._time_to_index(end_time)
            self.collection.update_one(
                {"user_id": user_id},
                {"$set": {f"availability.{i}": available for i in range(start_index, end_index)}}
            )

    def is_available(self, user_id, time):
        """Check if a user is available at a specific time."""
        self.initialize_user(user_id)
        index = self._time_to_index(time)
        user_data = self.collection.find_one({"user_id": user_id})
        return user_data["availability"][index]

    def find_availability(self, user_id, start_time, end_time):
        """Find all available slots within a given time range."""
        self.initialize_user(user_id)
        start_index = self._time_to_index(start_time)
        end_index = self._time_to_index(end_time)
        user_data = self.collection.find_one({"user_id": user_id})
        available_slots = []
        for i in range(start_index, end_index):
            if user_data["availability"][i]:
                available_slots.append(self._index_to_time(i))
        return available_slots

    def find_overlap(self, user1_id, user2_id):
        """Find overlapping available slots between two users."""
        self.initialize_user(user1_id)
        self.initialize_user(user2_id)
        user1_data = self.collection.find_one({"user_id": user1_id})
        user2_data = self.collection.find_one({"user_id": user2_id})
        overlap_slots = []
        for i in range(48):
            if user1_data["availability"][i] and user2_data["availability"][i]:
                overlap_slots.append(self._index_to_time(i))
        return overlap_slots

    def _time_to_index(self, time):
        """Convert a time string (HH:MM) to an index."""
        hours, minutes = map(int, time.split(':'))
        if hours < 0 or hours > 23 or minutes not in {0, 30}:
            raise ValueError("Invalid time format")
        return hours * 2 + (minutes // 30)

    def _index_to_time(self, index):
        """Convert an index to a time range string (HH:MM-HH:MM)."""
        hours = index // 2
        minutes = (index % 2) * 30
        start_time = f"{hours:02}:{minutes:02}"
        end_minutes = minutes + 30
        if end_minutes == 60:
            end_minutes = 0
            hours += 1
        end_time = f"{hours:02}:{end_minutes:02}"
        return f"{start_time}-{end_time}"
