class Train:
    def __init__(self, id=None, train_number="", train_name="", source="", destination="", departure_time="", arrival_time="", duration="", fare=0, total_seats=0, available_seats=0, class_type="General"):
        self.id = id
        self.train_number = train_number
        self.train_name = train_name
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.fare = fare
        self.total_seats = total_seats
        self.available_seats = available_seats
        self.class_type = class_type

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return Train(
            id=row["id"],
            train_number=row["train_number"],
            train_name=row["train_name"],
            source=row["source"],
            destination=row["destination"],
            departure_time=row["departure_time"],
            arrival_time=row["arrival_time"],
            duration=row["duration"],
            fare=row["fare"],
            total_seats=row["total_seats"],
            available_seats=row["available_seats"],
            class_type=row.get("class_type", "General"),
        )
