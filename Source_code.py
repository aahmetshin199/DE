import math
import numpy
import plotly
import plotly.graph_objs
 
class Equation(): #y' = sin(x) + y
 
    def get_derivative(self, x, y):  #local derivative
        return math.sin(x) + y
 
    def rad2deg(self, x): #converting radians to degrees
        return (2.0 * math.pi * x/360.0)
 
    def __init__(self, x0, y0, X, n): #initialization
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.n = n
 
        h = (X - x0)/n
        self.h = h
 
        self.x = numpy.arange(x0, X + 0.000001, h)
 
    def local_errors(self, ff):  #graph of local errors
 
        y = ff[1]
 
        y_error = [0] * len(self.x)
        ex = self.exact_solution()
 
        for i in range(len(self.x)):
            y_error[i] = abs(ex[1][i] - y[i])
            
        return [self.x, y_error]
 
    def max_error(self, ff):  #maximum error of function ff
 
        l = self.local_errors(ff)
        mx = 0
        a = l[1]
 
        return max(l[1])

        #for i in range(len(a))
        #	mx = max(mx, abs(a[i]))
 
        #return mx
 
    def exact_solution(self):
 
        c = (self.y0 + (math.sin(self.x0) + math.cos(self.x0)))/(math.e**self.x0)
        y = [0] * len(self.x)
 
        for i in range(len(self.x)):
            y[i] = c * (math.e**self.x[i]) - (math.sin(self.x[i]) + math.cos(self.x[i]))/2.0

        return [self.x, y]
 
 
class Numeric_methods():

    def euler_method(self, f):  #function got by Euler's method
 
        y = [0] * len(f.x)
        y[0] = f.y0
 
        for i in range(1, len(f.x)):
            y[i] = y[i - 1] + f.h * f.get_derivative(f.x[i - 1], y[i - 1]) #augmentation
 
        return [f.x, y]
 
    def euler_method_improved(self, f):   #function got by improved Euler's method
 
        y = [0] * len(f.x)
        y[0] = f.y0
 
        for i in range(1, len(f.x)):
            d = f.h * f.get_derivative(f.x[i - 1] + f.h/2, y[i - 1] + f.h/2 * f.get_derivative(f.x[i - 1], y[i - 1]))
            y[i] = y[i - 1] + d #augmentation
 
        return [f.x, y]
 
    def runge_kutta_method(self, f):   #function got by improved Runge-Kutta method
 
        y = [0] * len(f.x)
        y[0] = f.y0
 
        for i in range(1, len(f.x)):
 
            d1 = f.get_derivative(f.x[i - 1], y[i - 1])
            d2 = f.get_derivative(f.x[i - 1] + f.h/2, y[i - 1] + f.h * d1/2)
            d3 = f.get_derivative(f.x[i - 1] + f.h/2, y[i - 1] + f.h * d2/2)
            d4 = f.get_derivative(f.x[i - 1] + f.h,   y[i - 1] + f.h * d3)
 
            d = f.h * (d1 + 2 * d2 + 2 * d3 + d4)/6
            y[i] = y[i - 1] + d #augmentation
 
        return [f.x, y]
 
 
    def total_approximation_errors(self, start_n, end_n, x0, y0, X):
 
        euler_total_y = [0] * (end_n - start_n + 1)
        euler_improved_total_y = [0] * (end_n - start_n + 1)
        runge_kutta_total_y = [0] * (end_n - start_n + 1)
        total_x = [0] * (end_n - start_n + 1)
 
        for i in range(start_n, end_n + 1):
 
            j = i - start_n
            total_x[j] = i
 
            e = Equation(x0, y0, X, i)
 
            euler_result = (self.euler_method(e))
            euler_improved_result = (self.euler_method_improved(e))
            runge_kutta_result = (self.runge_kutta_method(e))   
 
            euler_total_y[j] = e.max_error(euler_result)
            euler_improved_total_y[j] = e.max_error(euler_improved_result)
            runge_kutta_total_y[j] = e.max_error(runge_kutta_result)
 
        euler_total = [total_x, euler_total_y]
        euler_improved_total = [total_x, euler_improved_total_y]
        runge_kutta_total = [total_x, runge_kutta_total_y]        
 
        return [euler_total, euler_improved_total, runge_kutta_total]

class Plotting():
    def plot(self, n, f, names, file):
        
        d = [0] * len(f)
        for i in range(len(f)):
            d[i] = plotly.graph_objs.Scatter(x = f[i][0], y = f[i][1], name = names[i], mode = "lines+markers")
        plotly.offline.plot(d, filename = file)
 
 
x0 = 0.0
y0 = 1.0
X = 2.4
N = 10
 
print("Please, print x0, y0, X, N in the console if want to change it and print 'no' otherwise. \n(print four values divided only by spaces, example: '1 2 3 4'")
s = input()
 
if s != "no":
    x0, y0, X, N = list(map(float, s.split()))

e = Equation(x0, y0, X, N)
 
euler_result = Numeric_methods().euler_method(e)
euler_improved_result = Numeric_methods().euler_method_improved(e)
runge_kutta_result = Numeric_methods().runge_kutta_method(e)
 
#print(euler_result[1])
#print(euler_improved_result[1])
#print(runge_kutta_result[1])
#print(e.exact_solution()[1])
Plotting().plot(N + 1, [euler_result, euler_improved_result, runge_kutta_result, e.exact_solution()], ["Euler Method", "Improved Euler Method", "Runge Kutta Method", "Exact Solution"], "result.html")
 
euler_error = e.local_errors(euler_result)
euler_improved_error = e.local_errors(euler_improved_result)
runge_kutta_error = e.local_errors(runge_kutta_result)

#print(euler_error[1])
#print(euler_improved_error[1])
#print(runge_kutta_error[1])
Plotting().plot(N + 1, [euler_error, euler_improved_error, runge_kutta_error], ["Euler Error", "Improved Euler Error", "Runge Kutta Error"], "local_errors.html")
 
print("Please, write starting and finishing values of the numbers of grid cells to provide the graph of total errors for each method for a given range")
 
start_n, end_n = list(map(int, input().split()))
 
total = Numeric_methods().total_approximation_errors(start_n, end_n, x0, y0, X)

Plotting().plot(end_n - start_n + 1, total, ["Euler Total Error", "Improved Euler Total Error", "Runge Kutta Total Error"], "total_errors.html")
