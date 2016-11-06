def unique(array):
	for i in range(len(array) - 1):
		for j in range(i + 1, len(array)):
			if (array[i] == array[j] and
				type(array[i]) == type(array[j])):
				return False
	return True
