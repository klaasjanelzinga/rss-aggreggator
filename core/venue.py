class Venue:

    def __init__(self, venue_id: str,
                 name: str,
                 url: str,
                 city: str,
                 country: str,
                 phone: str,
                 email: str):
        self.name = name
        self.url = url
        self.venue_id = venue_id
        self.email = email
        self.phone = phone
        self.city = city
        self.country = country
