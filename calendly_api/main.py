from services.availability_service import AvailabilityService
import unittest

def main():
    api = AvailabilityService()

    # Set user availability
    api.set_availability("user1", "09:00", "12:00", True)
    api.set_availability("user1", "14:00", "16:00", True)
    api.set_availability("user2", "10:00", "11:30", True)
    api.set_availability("user2", "15:00", "17:00", True)

    # Update user availability
    updates = [("09:00", "10:00", False), ("11:00", "12:00", True)]
    api.update_availability("user1", updates)

    # Check availability
    print(f"User1 is available at 10:30: {api.is_available('user1', '10:30')}")
    print(f"User1 is available at 09:30: {api.is_available('user1', '09:30')}")

    # Find available slots
    available_slots = api.find_availability("user1", "08:00", "11:00")
    print(f"User1 available slots between 08:00 and 11:00: {available_slots}")

    # Find overlap
    overlap = api.find_overlap("user1", "user2")
    print(f"Overlapping slots between User1 and User2: {overlap}")

    unittest.main()

if __name__ == "__main__":
    main()
