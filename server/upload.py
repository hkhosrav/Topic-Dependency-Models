import os

def saveData(filename, data):

    if not os.path.exists('uploads'):
        os.makedirs('uploads')


    target = os.path.join('uploads',filename)
    f = open(target, 'wb')
    f.write(data)
    f.close()
    return ("Success")
