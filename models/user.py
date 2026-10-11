class User:
    def __init__(self, id=None, name="", email="", password="", role="user"):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password=row["password"],
            role=row.get("role", "user"),
        )
