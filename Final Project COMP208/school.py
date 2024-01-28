import math
import numpy as np
import matplotlib.pyplot as plt
from student import Student

class School:
    def __init__(self, schoolName, studentList):
        self.schoolName = schoolName
        self.studentList = studentList
    

    def addStudent(self, ID:str, grades:list):
        s = Student(ID,grades)
  
        self.studentList.append(s)
        


    def highestStudent(self):
        avg_lst =[]
        for student in self.studentList:
            avg_lst.append(student.averageGrade())
        
        highest_ID = (self.studentList[avg_lst.index(max(avg_lst))]).studentID
        highest_avg = (self.studentList[avg_lst.index(max(avg_lst))]).averageGrade()
        
        return (highest_ID,highest_avg)
        
                
        
