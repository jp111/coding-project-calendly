class Availability:
    def __init__(self, user_id: str, slots: list = None):
        self.user_id = user_id
        self.slots = slots or [True] * 48

    @staticmethod
    def from_dict(data: dict):
        return Availability(user_id=data["user_id"], slots=data["availability"])

    def to_dict(self):
        return {"user_id": self.user_id, "availability": self.slots}
