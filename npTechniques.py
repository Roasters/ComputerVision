it = np.nditer(AA, flags=["multi_index"], op_flags=["readwrite"])
while not it.finished :
    idx = it.multi_index
    print(AA[idx])
    it.iternext()

list2 = [n for n in range(10, 90, 10)] 
AA = np.array(list2)
AA = A.reshape(2,4)
DD = np.concatenate((AA, np.array([1,2,3,4]).reshape(1,4)), axis=0)

data = np.loadtxt(r"C:\images\Etc_Raw\sdf.csv", delimiter=',', dtype=np.int32)