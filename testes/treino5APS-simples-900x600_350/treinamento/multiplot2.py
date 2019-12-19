import numpy as np
import matplotlib.pyplot as plt

def plotAP(plt, cx, cy, cor, lab):
	theta = np.linspace(0, 2*np.pi, 100)
	r = 250

	x = r*np.cos(theta) + cx
	y = r*np.sin(theta) + cy

	plt.plot(cx, cy, 'bo', color='black')
	plt.plot(x, y, color=cor, label=lab)

def plotAmb(ax):
	# background
	ax.set_facecolor('gray')
	# retangulo delimitador
	xmin, xmax, ymin, ymax = ax.axis([-10, 910, -10, 610])
	ax.plot(xlim=(xmin, xmax), ylim=(ymin, ymax))

	# AP1
	plotAP(ax, 275, 450, 'pink', 'AP1')
	# AP2
	plotAP(ax, 625, 450, 'red', 'AP2')
	# AP3
	plotAP(ax, 450, 150, 'green', 'AP3')
	# AP4
	plotAP(ax, 100, 150, 'orange', 'AP4')
	# AP5
	plotAP(ax, 800, 150, 'blue', 'AP5')

##############################################################

