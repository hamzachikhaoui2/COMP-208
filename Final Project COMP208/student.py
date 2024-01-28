import math
import numpy as np
import matplotlib.pyplot as plt

class Student:
    def __init__(self, studentID, gradesL):
        self.studentID = studentID
        self.gradesList = gradesL


    def addGrade(self, n):
        self.gradesList.append(n)

    def averageGrade(self):
        average_grade = 0
        
        for grade in self.gradesList:
        
            average_grade += grade
        average_grade  = average_grade/(len(self.gradesList))
        return (average_grade)

        

