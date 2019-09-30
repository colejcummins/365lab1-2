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

    grades = students_by_grade(students)

    while True:
        inp = input(prompt)
        split = inp.split()

        if check(split, "Info"):
            print("\n".join(str(i + 1) + ":" + str(grades[i]) for i in range(len(grades))))

        elif check(split, "Quit"):
            break

        elif check(split, "Average:", ":", 2):
            sum_gpa = 0.0
            for s in students:
                sum_gpa += float(s.GPA) if s.Grade == split[1] else 0
            if grades[int(split[1]) - 1] > 0:
                print(split[1], round(sum_gpa/grades[int(split[1]) - 1], 2))

        elif check(split, "Grade:", ":", 2):
            attr = ["StLastName", "StFirstName", "GPA", "Bus", "TLastName", "TFirstName"]
            if len(split) == 2:
                seq_search("Grade", split[1], attr, students)
            elif split[2] == "High" or split[2] == "H":
                high = Student(["", "", "", "", "", "0.0", "", ""])
                find_max_min(students, grades, split, attr, high, lambda a, b: float(a) > float(b))

            elif split[2] == "Low" or split[2] == "L":
                low = Student(["", "", "", "", "", "100.0", "", ""])
                find_max_min(students, grades, split, attr, low, lambda a, b: float(a) < float(b))

        elif check(split, "Teacher:", ":", 2):
            seq_search("TLastName", split[1], ["StLastName", "StFirstName"], students)

        elif check(split, "Bus:", ":", 2):
            seq_search("Bus", split[1], ["StLastName", "StFirstName", "Grade", "Classroom"], students)

        elif check(split, "Student:", ":", 2):
            if len(split) == 3 and (split[2] == "B" or split[2] == "Bus"):
                seq_search("StLastName", split[1], ["StLastName", "StFirstName", "Bus"], students)
            else:
                attrs = ["StLastName", "StFirstName", "Grade", "Classroom", "TLastName", "TFirstName"]
                seq_search("StLastName", split[1], attrs, students)

        print("")

def students_by_grade(students):
    grades = [0 for _ in range(6)]
    for s in students:
        grades[int(s.Grade) - 1] += 1
    return grades

def find_max_min(students, grades, split, attr, start, comp):
    for s in students:
        if s.Grade == split[1] and comp(s.GPA, start.GPA):
            start = s
    if grades[int(split[1]) - 1] > 0:
        print(",".join(getattr(start, a) for a in attr))

def check(split, word, add="", exp_len=1):
    return (split[0] == word or split[0] == word[0] + add) and len(split) >= exp_len

# attr: string, inp: string, print_attrs: list
# Takes the attribute to search, the given input, and a list of attributes to print, prints out all students within
# params
def seq_search(attr, inp, print_attrs, students):
    str = ""
    for s in students:
        if getattr(s, attr) == inp:
            str += ",".join(getattr(s, a) for a in print_attrs) + "\n"
    print(str)

if __name__ == "__main__":
    main()
