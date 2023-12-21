import numpy as np

class Dataset:
    """
    Dataset is a class for linear multidimensional interpolation.

    keys: 1D list of floats. Stores the independent variables associated with each index of 'data'
    data: 1D list of floats or Datasets. 
        If this Dataset is a base dataset 'data' holds floats. 
        If this Dataset is a parent dataset 'data' holds other Dataset objects 
    interp: method for recursive, multidimensional linear interpolation
    """
    def __init__(self, data=None, dependent_variables=1):
        """
        __init__ creates a Dataset. 
        If no value is passed in for data, the object is not fully initialized and initialization must be completed with init_from_file

        data: numeric Nx1 list of arrays, each row is a list of floats from one line of the text input file
        dependent_variables: the number of dependent variables stored in the data
        """
        if data!=None:
            self.__initialize(array_data=data, dependent_variables=dependent_variables)

    def init_from_file(self, filename, dependent_variables=1):
        """
        init_from_file finishes creating a Dataset, if the full data is not passed to __init__

        filename: string of the file to read in data from
        dependent_variables: the number of dependent variables stored in the data
        """
        with open(filename, 'r') as file:
            fileData = file.readlines()
        data = []
        for line in fileData:
            if len(line)>1:
                data.append([float(val) for val in line.split()])
        self.__initialize(data, dependent_variables)

    def __initialize(self, array_data, dependent_variables):
        """
        __initialize is an internal method which fills out the Dataset object
        """
        if len(array_data[0]) == (1+dependent_variables):
            keys = []
            data = []
            for arr in array_data:
                keys.append(arr[0])
                data.append(arr[1:])
            self.keys = keys
            self.data = data
        else: 
            stripped_data = [[]]
            independent_value = array_data[0][0]
            keys = [independent_value]
            for arr in array_data:
                if arr[0] != independent_value:
                    independent_value = arr[0]
                    keys.append(arr[0])
                    stripped_data.append([arr[1:]])
                else:
                    stripped_data[-1].append(arr[1:])
            self.data = []
            for arr in stripped_data:
                self.data.append(Dataset(arr, dependent_variables=dependent_variables))
            self.keys = keys

    def interp(self, v):
        """
            interp linearly interpolates recursively through Datasets
            When it is called it recurses to the base, numeric data, which it linearly interpolates.
            Then, it goes back through each level, linearly interpolating with the numeric data from the sub-level.
            It passes the numeric interpolation result up a level.
            
            param v: an n-dimensional vector. Each recursive iteration strips one value, until in the final iteration v is 1x1.
        """

        #Come up with the list indices and weights between indices for linear interpolation
        idx,weight = -1,-1
        if(v[0]<self.keys[0]):
            idx, weight = 0,0
            raise ValueError("Data to be interpolated is below the range of tabulated data")
        elif(v[0]>self.keys[-1]):
            idx, weight = len(self.keys)-1, 1
            raise ValueError("Data to be interpolated is above the range of tabulated data")
        else:
            for i in range(len(self.keys)-1):
                if(v[0]>=self.keys[i] and v[0]<self.keys[i+1]):
                    idx=i
                    weight = (v[0]-self.keys[i]) / (self.keys[i+1]-self.keys[i])
                    break
        assert weight >= 0.0, f"Weight must be greater than 0, it is {weight}"
        assert idx >= 0, "List index cannot be negative"

        #Linearly interpolate, numerically if data is numeric or recursively if data is other Datasets
        if len(v)==1:
            return (1-weight)*np.array(self.data[idx]) + (weight)*np.array(self.data[idx+1])
        else:
            return (1-weight)*np.array(self.data[idx].interp(v[1:])) + (weight)*np.array(self.data[idx+1].interp(v[1:]))
