import numpy as np

def genData(funcs, nPoints, dataRange, filename='data.txt', v=None, varIdx=-1, fileContents=None, random=False):
    """
    genData: function to generate text data of the form 'idpt1 idpt2 idpt3 dpdt1 dpdt2 \n' (for N=3)
    
    funcs - the N-dimensional functions to generate dependent data from. Must be of the same dimension
    nPoints - Nx1 vector with the number of points to generate in each dimension
    dataRange - Nx2 vector with the minimum and maximum of each data range
    filename - the filename to store the data in
    random - if False, points linearly spaced. if True, amount of points is scaled randomly and points are distributed randomly
        Used to demonstrate code's capability to handle non-uniform data.
    """

    if varIdx == -1:
        v = np.zeros((len(nPoints), 1))
        fileContents = ''
        fileContents = genData(funcs, nPoints, dataRange, filename=filename, fileContents=fileContents, varIdx=0, v=v, random=random)
        with open(filename, 'w+') as file:
            file.write(fileContents)
    elif varIdx == len(nPoints) - 1:  # last
        if(random):
            randoms = np.random.uniform(dataRange[varIdx][0], dataRange[varIdx][1], nPoints[varIdx]+np.random.randint(1,6))
            space = np.sort(randoms)
        else:
            space = np.linspace(dataRange[varIdx][0], dataRange[varIdx][1], nPoints[varIdx])

        for point in space:
            v[-1] = point
            val = ' '
            for func in funcs:
                val += str(func(v).item()) + ' '
            fileContents += ' '.join(map(str, v.flatten())) + val + ' \n'
    else:
        if(random):
            randoms = np.random.uniform(dataRange[varIdx][0], dataRange[varIdx][1], nPoints[varIdx]+np.random.randint(1,6))
            space = np.sort(randoms)
        else:
            space = np.linspace(dataRange[varIdx][0], dataRange[varIdx][1], nPoints[varIdx])

        for point in space:
            v[varIdx] = point
            fileContents = genData(funcs, nPoints, dataRange, filename=filename, fileContents=fileContents, varIdx=varIdx + 1, v=v, random=random)
    return fileContents
