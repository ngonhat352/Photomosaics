# %%writefile 13reductionList.py
from mpi4py import MPI

# Exercise: Can you explain what this function returns,
#           given two lists as input?
def sumListByElements(x,y):
    return [a+b for a, b in zip(x, y)]

def main():
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()            #number of the process running the code
    numProcesses = comm.Get_size()  #total number of processes running
    myHostName = MPI.Get_processor_name()  #machine name running the code

    srcList = [1*id, 2*id, 3*id, 4*id, 5*id]
    print(srcList)
    destListMax = comm.reduce(srcList, op=MPI.MAX)
    destListSum = comm.reduce(srcList, op=MPI.SUM)
    #destListSumByElement = comm.reduce(srcList, op=sumListByElements)

    if id == 0:        # master/root process will print result
        print("The resulting reduce max list is  {}".format(destListMax))
        print("The resulting reduce sum list is  {}".format(destListSum))
        #print("The resulting reduce sum list is  {}".format(destListSumByElement))

########## Run the main function
main()

# from mpi4py import MPI
#
# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# size = comm.Get_size()
#
# print('INIT')
# comm.Barrier()
# print('BEFORE')
# comm.Barrier()
# print('AFTER')

# from mpi4py import MPI
# # from mpi4py import MPI
#
# # Create a list of lists to be scattered.
# def genListOfLists(numElements):
#     data = [[0]*3 for i in range(numElements)]
#     for i in range(numElements):
#         #make small lists of 3 distinct elements
#         smallerList = []
#         for j in range(1,4):
#             smallerList = smallerList + [(i+1)*j]
#         # place the small list in the larger list
#         data[i] = smallerList
#     return data
#
# def main():
#     comm = MPI.COMM_WORLD
#     id = comm.Get_rank()            #number of the process running the code
#     numProcesses = comm.Get_size()  #total number of processes running
#     myHostName = MPI.Get_processor_name()  #machine name running the code
#
#     # in mpi4py, the lowercase scatter method only works on lists whose size
#     # is the total number of processes.
#     numElements = numProcesses      #total elements in list created by master process
#
#     # however, the list can contain lists, like this list of 3-element lists,
#     # for example this list of four 3-element lists:
#     #     [[1, 2, 3], [2, 4, 6], [3, 6, 9], [4, 8, 12]]
#
#     if id == 0:
#         data = genListOfLists(numElements)
#         print("Master {} of {} on {} has created list: {}"\
#         .format(id, numProcesses, myHostName, data))
#     else:
#         data = None
#         print("Worker Process {} of {} on {} starts with {}"\
#         .format(id, numProcesses, myHostName, data))
#
#     #scatter one small list in the large list on node 0 to each of the processes
#     result = comm.scatter(data, root=0)
#
#     print("Process {} of {} on {} has result after scatter {}"\
#     .format(id, numProcesses, myHostName, result))
#
#     if id == 0:
#         print("Master {} of {} on {} has original list after scatter: {}"\
#         .format(id, numProcesses, myHostName, data))
#
# ########## Run the main function
# main()
# def main():
#     print('aa')
#     comm = MPI.COMM_WORLD
#     rank = comm.Get_rank()
#     print(rank)
#     comm.Barrier()
#     MPI.COMM_WORLD.Barrier()
#     print('bb')
#     # print("aa")
#     # comm = MPI.COMM_WORLD
#     # id = comm.Get_rank()            #number of the process running the code
#     # numProcesses = comm.Get_size()  #total number of processes running
#     # myHostName = MPI.Get_processor_name()  #machine name running the code
#     #
#     # print("Greetings from process {} of {} on {}"\
#     # .format(id, numProcesses, myHostName))
#
# if __name__ == '__main__':
#     main()
