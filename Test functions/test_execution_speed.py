def show_bar(times):
	import matplotlib.pyplot as plt
	categories = range(len(times))
	values = []
	for i in times:
		values.append(sum(i) / len(i))

	plt.bar(categories, values, color="orange")
	plt.title("Время на обработку")
	plt.xlabel('Часть кода')
	plt.ylabel('Время')
	plt.show()
	plt.savefig("aboba.png")

time_values = []
time_index = 0

def add_time(t):
	global time_index
	if len(time_values) <= time_index:
		time_values.append([])
	time_values[time_index].append(t)
	time_index += 1
def reset_time():
	global time_index
	time_index = 0
