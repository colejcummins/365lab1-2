# A class representing a student
class Student:
    def __init__(self, args):
        self.StLastName = args[0]
        self.StFirstName = args[1]
        self.Grade = args[2]
        self.Classroom = args[3]
        self.Bus = args[4]
        self.GPA = args[5]
        self.TLastName = args[6]
        self.TFirstName = args[7]

def read_file(filename, arr, func, *kwargs):
    with open(filename) as fp:
        line = fp.readline().strip()
        while line:
            split = line.replace(" ", "").split(",")
            func(arr, split, *kwargs)
            line = fp.readline().strip()

def add_students(arr, split, teachers):
    arr.append(Student(split + teachers[split[3]].split(",")))

def add_teachers(dict, split, *kwargs):
    dict[split[2]] = split[0] + "," + split[1]

def main():
    teachers = {}
    read_file("teachers.txt", teachers, add_teachers)
    students = []
    read_file("list.txt", students, add_students, teachers)
    prompt_loop(students)

def prompt_loop(students):
    prompt = str('Please enter a query. Example queries:\nS[tudent]: <lastname>'
    '[B[us]]\nT[eacher]: <lastname>\nB[us]: <number>\nG[rade]: <number>'
    '[H[igh]|L[ow]]\nA[verage]: <number>\nI[nfo]\nQ[uit]\n\n')

    while True:
        inp = input(prompt)
        split = inp.split()

        if check(split[0], "Info"):
            grades = [0 for _ in range(6)]
            for s in students:
                grades[int(s.Grade) - 1] += 1
            print("\n".join(str(i + 1) + ":" + str(grades[i]) for i in range(len(grades))))

        if check(split[0], "Quit"):
            break

        if len(split) < 2:
            continue

        if check(split[0], "Teacher:", ":"):
            seq_search("TLastName", split[1], ["StLastName", "StFirstName"], students)

        if check(split[0], "Bus:", ":"):
            seq_search("Bus", split[1], ["StLastName", "StFirstName", "Grade", "Classroom"], students)

        if check(split[0], "Student:", ":"):
            if len(split) == 3 and (split[2] == "B" or split[2] == "Bus"):
                seq_search("StLastName", split[1], ["StLastName", "StFirstName", "Bus"], students)
            else:
                attrs = ["StLastName", "StFirstName", "Grade", "Classroom", "TLastName", "TFirstName"]
                seq_search("StLastName", split[1], attrs, students)

        print("")


def check(inp, word, add=""):
    return inp == word or inp == word[0] + add

if __name__ == "__main__":
    main()

# attr: string, inp: string, print_attrs: list
# Takes the attribute to search, the given input, and a list of attributes to print, prints out all students within
# params
def seq_search(attr, inp, print_attrs, students):
    str = ""
    for s in students:
        if getattr(s, attr) == inp:
            str += ",".join(getattr(s, a) for a in print_attrs) + "\n"
    print(str)
