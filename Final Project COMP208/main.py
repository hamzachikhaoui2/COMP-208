import math
import numpy as np
import matplotlib.pyplot as plt
from school import School
from student import Student


def Main():
    studentList = []
    school = School("McGill",studentList)
    school.addStudent("1234", [3,4,5])
    school.addStudent("2345", [10,4,5])
    school.addStudent("2445", [10,20,5])

    print(school.highestStudent())
    



