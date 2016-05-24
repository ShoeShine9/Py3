class Person:
    def __init__(self, first_name, last_name, id_number):
        self.first_name = first_name
        self.last_name = last_name
        self.id_number = id_number

    def printPerson(self):
        print('Name:', self.last_name + ',', self.first_name)
        print('ID:', self.id_number)


class Student(Person):
    def __init__(self, first_name, last_name, id_number, scores=[]):
        super().__init__(first_name, last_name, id_number)
        int_scores = []
        for num in scores:
            int_scores.append(int(num))
        self.scores = int_scores

    def calculate(self):
        average = sum(self.scores)/len(self.scores)
        if average >= 90:
            return "O"
        if average >= 80:
            return "E"
        if average >= 70:
            return "A"
        if average >= 55:
            return "P"
        if average >= 40:
            return "D"
        if average >= 0:
            return "T"
