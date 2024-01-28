import matplotlib.pyplot as plt
import math
import time
import scipy.integrate as integrate
import numpy as np

def midpoint_integrate(f, a, b, N):
    area = 0.0
    dx = (b - a) / N # width of segment
    x = a # start segments at a
    for i in range(N):
        area += dx * f(x + dx / 2)
        x += dx # go to next segment     
    return area

def trapezoidal_integrate(f, a, b, N):
    area = 0.0
    dx = (b - a) / N
    x = a
    for i in range(N):
        area += dx * (f(x) + f(x + dx)) / 2
        x += dx
    return area

def simpsons_integrate(f, a, b, N):
    area = 0.0
    dx = (b - a) / N
    x = a  
    for i in range(N):
        area += dx * (f(x) + 4*f(x + dx / 2)
                       + f(x + dx)) / 6
        x += dx
    return area


def function(x):
    return 1 / (1+x**2)


def error(value):
    return abs(math.atan(5)-value)

def compute_error(method, N):
    error_vals = []
    for n in N:
        num_val = method(function, 0.0, 5.0, n)
        error_vals.append(error(num_val))
    return error_vals

def compute_time(method, N):
    time_vals = []
    for n in N:
        start = time.time()
        method(function, 0.0, 5.0, n)
        end = time.time()
        time_vals.append(end-start)
    return time_vals

def compute_time_sp(N):
    time_vals = []
    for n in N:
        x = [i for i in np.arange(0, 5.01, 5.0/n)]
        y = [function(i) for i in np.arange(0, 5.01, 5.0/n)]
        start = time.time()
        integrate.trapz(y, x)
        end = time.time()
        time_vals.append(end-start)
    return time_vals

def plot_time_trap():
    N = [10*(i**2) for i in range (1, 25)]
    trap = compute_time(trapezoidal_integrate, N)
    sp_trap = sompute_time_sp(N)
    plt.plot(N, trap, 'bs-', label = 'trapezoidal')
    plt.plot(N, sp_trap, 'g^-', label = 'scipy_trap')
    plt.legend()
    plt.show()
        

    

def plot_errors():
    N = [i for i in range (1,100)]
    mid = compute_error(midpoint_integrate, N)
    trap = compute_error(trapezoidal_integrate, N)
    simp = compute_error(simpsons_integrate, N)
    plt.plot(N, mid, 'r-', label = 'midpoint')
    plt.plot(N, trap, 'bs-', label = 'trapezoidal')
    plt.plot(N, simo, 'g^-', label = 'simpsons')
    plt.ylim(0, 0.1)
    plt.xlim(0, 10)
    plt.legend()
    plt.show()
    
def plot_times():
    N = [i for i in range (1,100)]
    mid = compute_error(midpoint_integrate, N)
    trap = compute_error(trapezoidal_integrate, N)
    simp = compute_error(simpsons_integrate, N)
    plt.plot(N, mid, 'r-', label = 'midpoint')
    plt.plot(N, trap, 'bs-', label = 'trapezoidal')
    plt.plot(N, simo, 'g^-', label = 'simpsons')
    plt.legend()
    plt.show

def f(x):
    return math.cos(x)

def plot_sin_cos():
    x = np.arange(-math.pi, math.pi + 0.1, 0.1)
    y_sin = [math.sin(e) for e in x]
    y_cos_integrated = []
    for element in x:
        y_cos_integrated.append(integrate.quad(f, -math.pi, element)[0])
    plt.plot(x, y_sin, 'bs-', label = 'sin()')
    plt.plot(x, y_cos_integrated, 'g^-', label = 'cos int')
    plt.legend()
    plt.show()

    
    
    
    
