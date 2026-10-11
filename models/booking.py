class Booking:
    def __init__(self, id=None, pnr="", user_id=None, train_id=None, passenger_name="", age=0, gender="", journey_date="", class_name="", seat_number=None, status="CONFIRMED", booking_time=""):
        self.id = id
        self.pnr = pnr
        self.user_id = user_id
        self.train_id = train_id
        self.passenger_name = passenger_name
        self.age = age
        self.gender = gender
        self.journey_date = journey_date
        self.class_name = class_name
        self.seat_number = seat_number
        self.status = status
        self.booking_time = booking_time

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Booking(
            id=row["id"],
            pnr=row["pnr"],
            user_id=row["user_id"],
            train_id=row["train_id"],
            passenger_name=row["passenger_name"],
            age=row["age"],
            gender=row["gender"],
            journey_date=row["journey_date"],
            class_name=row["class"],
            seat_number=row.get("seat_number"),
            status=row.get("status", "CONFIRMED"),
            booking_time=row.get("booking_time", ""),
        )
