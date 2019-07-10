import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from rocketcea.cea_obj import CEA_Obj, add_new_propellant
import numpy as np


""" define functions """
def kilojoule2cal(kilojoule):
	return kilojoule/4.184*1000

def bar2psi(bar):
	return bar*14.504

def createPropellant(wt1,wt2,wt3):
	card_str = """
	name H2O   H 2 O 1   wt%={:.1f}
	h,kj/mol=-285.8       t(k)=293.15
	name Methanol   C 1 H 4 O 1   wt%={:.1f}
	h,kj/mol=-239.2       t(k)=293.15
	name ADN   H 4 N 4 O 4   wt%={:.1f}
	h,kj/mol=-134.6       t(k)=293.15
	""".format(wt1,wt2,wt3)
	add_new_propellant("WaterMethanolADN_Mix",card_str)

def calculatePerformance(chamber_pressure,expansion_ratio):
	# chamber pressure in bar
	temp = CEA_Obj(propName="WaterMethanolADN_Mix")
	(isp,cstr,tc) = temp.getFrozen_IvacCstrTc(Pc=bar2psi(chamber_pressure),eps=expansion_ratio,frozenAtThroat=1)
	tc /= 1.8 # convert from rankine to kelvin
	return (isp, tc)

def cost(tc,isp):
	""" Target: Maximize ISP, stay below 1000C chamber temperature """
	if tc >= 1273.15:
		# greatly increase cost if temperature is to high
		return tc/isp
	else:
		# if below 1000C, invert ISP because optimizer will minimize
		return 1/isp



""" search for good composition """
chamber_pressure = 16 # bar
expansion_ratio = 60

# init results
results = []

# grid search
for wt1 in range(0,101,1):
	for wt2 in range(0,101-wt1,1):
		wt3 = 100 - wt1 - wt2
		try:
			# create new mixture
			createPropellant(wt1,wt2,wt3)
			# calc performance
			isp, tc = calculatePerformance(chamber_pressure,expansion_ratio)
			if isp != 0.0:
				# save in to results list
				results.append((wt1,wt2,wt3,isp,tc))
				# print
				print('Calculating Mixture of ',wt1,wt2,wt3,' WATER/METHANOL/ADN, ISP @',isp)
		except:
			print('Invalid mixture of ',wt1,wt2,wt3)

# stack list
results = np.vstack(results)

# delete zero isp mixtures
nonzero_row_indices =[i for i in range(results.shape[0]) if not results[i,3]==0]
data = results[nonzero_row_indices,:]

# save results
np.savetxt('b3/gridsearch.txt',results, header='#wt1\twt2\twt3\tisp[s]\ttc[K]')
		
""" plotting """
# create data matrices
isp_mat = np.zeros([101,101])
tc_mat = np.zeros([101,101])
tc_mask = np.zeros([101,101])
for i in range(results.shape[0]):
	x = int(results[i,2])
	y = int(results[i,1])
	isp_mat[x,y] = results[i,3]
	tc_mat[x,y] = results[i,4] - 273.15
	if tc_mat[x,y] < 1273.15:
		tc_mask[x,y] = 1	

# FIRST PLOT
# init plot
fig = plt.figure()
ax = fig.add_subplot(111)

# plot isp
im = ax.matshow(isp_mat, cmap='Greens')
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel("ISP", rotation=90, va="top")

# add labels
ax.set_xlabel('ADN %')
ax.set_ylabel('Methanol %')

# add max
max_isp = np.max(isp_mat)
arg_max_isp = np.unravel_index(np.argmax(isp_mat, axis=None), isp_mat.shape)
t_at_max_isp = tc_mat[arg_max_isp]
ax.text(2,22,
	'Maximum ISP {:.2f}s\nCombustion Temperature {:.2f}K\n{:d}% Methanol\n{:d}% ADN\n{:d}% H2O'.format(max_isp,t_at_max_isp,arg_max_isp[1],arg_max_isp[0],100-np.sum(arg_max_isp)),
	color="tomato")
ax.plot(arg_max_isp[1],arg_max_isp[0],'r+')

# adjust plots
plt.subplots_adjust(hspace=0.2)

# save fig
plt.savefig('b3/results.pdf')

# SECOND PLOT

isp_mat = np.multiply(tc_mask,isp_mat)

# init plot
fig = plt.figure()
ax = fig.add_subplot(111)

# plot isp
im = ax.matshow(np.multiply(isp_mat,tc_mask), cmap='Greens')
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel("ISP", rotation=90, va="top")
	
# add labels
ax.set_xlabel('ADN %')
ax.set_ylabel('Methanol %')

# add max
max_isp = np.max(isp_mat)
arg_max_isp = np.unravel_index(np.argmax(isp_mat, axis=None), isp_mat.shape)
t_at_max_isp = tc_mat[arg_max_isp]

ax.text(2,22,
	'Maximum ISP {:.2f}s\nCombustion Temperature {:.2f}K\n{:d}% Methanol\n{:d}% ADN\n{:d}% H2O'.format(max_isp,t_at_max_isp,arg_max_isp[1],arg_max_isp[0],100-np.sum(arg_max_isp)),
	color="tomato")
ax.plot(arg_max_isp[1],arg_max_isp[0],'r+')

# adjust plots
plt.subplots_adjust(hspace=0.2)

# save fig
plt.savefig('b3/results_masked.pdf')
