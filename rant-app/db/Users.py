class Users:
    def __init__(self, username, email, first_name, last_name, display_name):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.display_name = display_name
        self.interests = []
        self.rants = []
        self.isCounselor = False

    def add_interests(self, interests):
        self.interests = interests

    def set_counselor(self, isCounselor):
        self.isCounselor = isCounselor



