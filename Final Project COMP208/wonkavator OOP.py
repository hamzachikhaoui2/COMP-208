import math
from random import randint
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

plt.ion() # enable interactive mode (continue graphing without having to close the window)
plt.show() # show the plot

def sign(x):
    # Return the sign of x (0 if x is 0).
    if x > 0: # x positive
        return 1
    elif x < 0: # x negative
        return -1
    else: # x zero
        return 0

class Point3D():    
    def __init__(self, x, y, z): # class constructor
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
    
    def __eq__(self, other): # comparison
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __str__(self): # string representation
        return '<{}, {}, {}>'.format(self.x, self.y, self.z)
    
    def add(self, other): # add two points together
        return Point3D(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def distance(self, other): # get distance between two points
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)
    
    def get_direction_vector(self, other):
        # Return a vecotr of 1, 0 or -1 in each dimension corresponding to
        # the direction you would have to move from the self point to get to the other point.
        return Point3D(sign(other.x-self.x), sign(other.y-self.y), sign(other.z-self.z))
    
    def aslist(self): # Return the Point2D object as a list of three numbers.
        return [self.x, self.y, self.z]

def get_random_point(x0, x1, y0, y1, z0, z1):
    # return a Point3D object with random coordinates within the given x,y,z intervals.
    return Point3D(randint(x0, x1), randint(y0, y1), randint(z0, z1))

class Person:
    def __init__(self, name, cur_pos, dst_pos): # class constructor
        self.name = name
        self.cur_pos = cur_pos
        self.dst_pos = dst_pos
        self.arrived = False
    
    def arrive_at_destination(self):
        self.cur_pos = self.dst_pos
        self.arrived = True
        
    def __str__(self): # string representation
        return "Name:" + self.name + "; cur: " + str(self.cur_pos) + "; dst:" + str(self.dst_pos)

class Factory:
    def __init__(self, factory_size, people, elevator): # class constructor
        self.factory_size = factory_size
        self.people = people
        self.elevator = elevator
        
        self.axes = plt.axes(projection='3d')
    
    def run(self):
        '''This method is the main loop for the simulation and it operates the elevator. Particularly, this function checks if the elevator is currently in a room where there are people who want to enter the elevator, and/or if there are people in the elevator whose destination point is the current room and who thus want to leave the elevator.
        '''
        #A for loop  going through each Person object in a list of people
        for person in self.people:
            #If there is a person(s) who are in the elevator 
            if person in self.elevator.people_in_elevator:
                #if the person's destination is the current room
                if person.dst_pos == self.elevator.cur_pos:
                    #the person need to be dropped off in the room
                    self.elevator.person_leaves(person)
            else: #If there is a person(s) who are in the same room as the elevator and need to be picked up
                #making sure that the person does need to be picked up and has not already arrived at their destination room 
                if person.cur_pos == self.elevator.cur_pos and not person.arrived:
                    #the person need to be picked up
                    self.elevator.person_enters(person)
        
        if not self.is_finished():
            self.elevator.move(self.people)
    
    def show(self): # display the grid
        self.axes.clear() # clear the previous window contents
        
        # set the axis bounds
        self.axes.set_xlim(0, factory_size.x)
        self.axes.set_ylim(0, factory_size.y)
        self.axes.set_zlim(0, factory_size.z)
        self.axes.set_xticks(list(range(factory_size.x+1)))
        self.axes.set_yticks(list(range(factory_size.y+1)))
        self.axes.set_zticks(list(range(factory_size.z+1)))
        
        # show a blue dot for each person not yet in the elevator / not yet arrived at their destination
        xs, ys, zs = [], [], []
        for person in self.people:
            if not person.arrived and person not in self.elevator.people_in_elevator:
                xs.append(person.cur_pos.x)
                ys.append(person.cur_pos.y)
                zs.append(person.cur_pos.z)
        self.axes.scatter3D(xs, ys, zs, color='blue')
        
        # show a red dot for the destinations of the people currently in the elevator
        edxs, edys, edzs = [], [], []
        for person in self.people:
            if person in self.elevator.people_in_elevator:
                edxs.append(person.dst_pos.x)
                edys.append(person.dst_pos.y)
                edzs.append(person.dst_pos.z)
        self.axes.scatter3D(edxs, edys, edzs, color='red')
        
        # show a green dot for the elevator itself
        self.axes.scatter3D([self.elevator.cur_pos.x], [self.elevator.cur_pos.y], [self.elevator.cur_pos.z], color='green')
        
        plt.draw()
        plt.pause(0.5)
    
    def is_finished(self):
        return all(person.arrived for person in self.people)
    
class Wonkavator:
    def __init__(self, factory_size): # class constructor
        self.cur_pos = Point3D(0, 0, 0)
        self.factory_size = factory_size
        self.people_in_elevator = [] # the list of people currently in the elevator
        
    def move(self, people): # move the elevator
        # get the direction in which to move      
        direction = self.choose_direction(people)
        
        # check if the direction is correct
        if any(not isinstance(d, int) for d in direction.aslist()):
            raise ValueError("Direction values must be integers.")
        if any(abs(d) > 1 for d in direction.aslist()):
            raise ValueError("Directions can only be 0 or 1 in any dimension.")
        if all(d == 0 for d in direction.aslist()):
            raise ValueError("The elevator cannot stay still (direction is 0 in all dimensions).")
        if any(d < 0 or d > s for d, s in zip(self.cur_pos.add(direction).aslist(), self.factory_size.aslist())):
            raise ValueError("The elevator cannot move outside the bounds of the grid.")
                
        # move the elevator in the correct direction
        self.cur_pos = self.cur_pos.add(direction)
        
    def choose_direction(self, people):
        if len(self.people_in_elevator) == 0: # if thre is no one in elevator yet
            # find the person closest to the elevator's position
            closest_dist = math.inf
            #looping through all the people
            for person in people:
                #if the specific person has not already arrived to the destination
                if not person.arrived and person not in self.people_in_elevator:
                    #compute the distance of the position of person with respect to the current position of the elevator
                    dist = person.cur_pos.distance(self.cur_pos)
                    #check if the distant of the current person is less that the minimum distance found so far
                    if dist < closest_dist:
                        #update the distance
                        closest_dist = dist
                        
                        # change direction to be one unit in their direction
                        direction = self.cur_pos.get_direction_vector(person.cur_pos)
        else:
            # find the closest destination of all people in elevator
            closest_dist = math.inf
            #looping throug all the people
            for person in self.people_in_elevator:
                #compute the distance of the destination position of person with respect to the current position of the elevator
                dist = person.dst_pos.distance(self.cur_pos)
                #check if the distant of the current person is less that the minimum distance found so far
                if dist < closest_dist:
                    #update the distance
                    closest_dist = dist
            
                    # change direction to be one unit in their direction
                    direction = self.cur_pos.get_direction_vector(person.dst_pos)
        
        return direction
    
    def person_enters(self, person): # person arrives in elevator
        if person.arrived:
            raise Exception("A person can only enter the elevator if they have not yet reached their destination.")
        
        self.people_in_elevator.append(person) # add them to the list
    
    def person_leaves(self, person): # person departs elevator
        if person.dst_pos != elevator.cur_pos:
            raise Exception("A person can only leave the elevator if the elevator has reached their destination point.")
        
        person.arrive_at_destination() # let the person know they have arrived
        self.people_in_elevator.remove(person) # remove them from the list

if __name__ == '__main__':    
    factory_size = Point3D(5, 5, 5)
    
    # create the people objects
    people = []
    pos_current = [(0, 0, 1), (3, 3, 1), (1, 2, 4), (0, 2, 4), (1, 4, 3), (0, 3, 0), (2, 0, 2), (2, 1, 0)]
    pos_destination = [(0, 2, 1), (0, 4, 2), (0, 1, 0), (4, 4, 3), (1, 2, 1), (1, 1, 2), (0, 2, 4), (3, 3, 0)]
    names = ["Joseph", "David", "Belle", "Cecily", "Faizah", "Nabila", "Tariq", "Benn"]
    
    for index in range(len(names)):
        cur = Point3D(pos_current[index][0], pos_current[index][1], pos_current[index][2])
        dst = Point3D(pos_destination[index][0], pos_destination[index][1], pos_destination[index][2])
        people.append(Person(names[index], cur, dst))

    # create the elevator
    elevator = Wonkavator(factory_size)
    
    # create the factory
    factory = Factory(factory_size, people, elevator)
    
    while True:
        factory.run() #
        factory.show()
        
        # check if everyone has arrived at their destinations
        if factory.is_finished():
            break
        
    print("Everyone has arrived.")
