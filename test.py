import dataset
import generate_data
import numpy as np

def f(v):
    x,y=v
    return x**2+y**2
def g(v):
    x,y=v
    return abs(x+y)

def h(v):
    x,y,z,w = v
    return (abs(x*y*z*w))**(1./5.) + np.cos(x*y) - np.sin(z*w)

def k(v):
    x,y,z,w = v
    return abs(x+y**(2)) - abs(z)**(w/10.)

#Demo: interpolate 2 functions with 2 dependent variables
filename = 'test3D.txt'
#Because the random option is used in generating data, the data will be non-uniform
#As a result, the test vector can fall outside the generated data range. Run again if this happens
generate_data.genData([f,g],[100,100],[[-5,5],[-5,5]], filename=filename, random=True)
data = dataset.Dataset()
data.init_from_file(filename, dependent_variables=2)
testVector = [-2.34,4.567]
print(f"For 1st function, interpolated value is {data.interp(testVector)[0]} compared to expected result {f(testVector)}")
print(f"For 2nd function, interpoalted value is {data.interp(testVector)[1]} compared to expected result {g(testVector)}")

#Demo: interpolate 2 functions with 4 independent variables
filename = 'test5D.txt'
generate_data.genData([h,k],[5,10,30,20],[[-5,5],[-5,5],[-5,5],[-5,5]], filename=filename)
data = dataset.Dataset()
data.init_from_file(filename, dependent_variables=2)
testVector = [3.64,-1.99,1.15,0.12]
print(f"For 1st function, interpolated value is {data.interp(testVector)[0]} compared to expected result {h(testVector)}")
print(f"For 2nd function, interpoalted value is {data.interp(testVector)[1]} compared to expected result {k(testVector)}")


