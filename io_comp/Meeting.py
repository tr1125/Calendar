class Meeting:
    def __init__(self, person_name, name, start_time, end_time):
        self.person_name = person_name
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"Meeting(Person: {self.person_name}, Name: {self.name}, Start Time: {self.start_time}, End Time: {self.end_time})"