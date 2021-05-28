import numpy as np
def less(a, b):
	for i in range(len(a)):
		if a[i] > b[i]:
			return False
	return True
def add(a, b):
	c = [0]*len(a)
	for i in range(len(a)):
		c[i] = a[i] + b[i]
	return c
def banker(max, allocation, available, need):
	# print(max, allocation, available, need, sep='\n')
	m, n = np.shape(max)
	work = available
	finish = [False]*m
	print('need', need)
	while True:
		find = False
		for i in range(m):
			if less(need[i], work) and finish[i] == False:
				print('i =', i)
				work = add(work, allocation[i])
				finish[i] = True
				find = True
				print('Need[{}] ='.format(i),need[i],'<= Work')
				print('Work += Allocation[{}] ='.format(i), work)
				print('Finish = ',finish)
				break
			if finish == [True, True, True, True, True]:
				return 'safe'
		if find == False:
			return 'unsafe'


allocation = np.array([[0,1,0], [2,0,0], [3,0,1], [2,1,1], [0,0,2]])
max = np.array([[7,5,3], [3,2,2], [9,0,2], [2,2,2], [4,3,3]])

available = [3,3,2]
need = np.subtract(max, allocation)
# need = np.array([[1,0,0], [2,0,2], [0,0,1], [1,0,0], [0,0,2]])
# print(need)

def resources_allocation(max, allocation, available, need, i, request):
	if less(request, need[i]):
		if less(request, available):
			available = np.subtract(available, request)
			print('Available -= Request[{}] ='.format(i), available)
			allocation[i] = np.add(allocation[i], request)
			print('Allocation[{}] += Request[{}] ='.format(i,i), allocation[i])
			need[i] = np.subtract(need[i], request)
			print('Need[{}] -= Request[{}] ='.format(i, i), need[i])
			print('\ndetermine if this state is safe:\n')
			return banker(max, allocation, available, need)
		else:
			return 'no more available resources'
	else:
		return 'max exceeded'	
# print(banker(max,allocation,available,need))
print(resources_allocation(max, allocation, available, need, 1, [1,0,2]))