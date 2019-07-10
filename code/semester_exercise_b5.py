import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from rocketcea.cea_obj import CEA_Obj, add_new_propellant
import numpy as np

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
	
def bar2psi(bar):
	return bar*14.504
	
""" prepare fuel """
meth = 39
adn = 59
h2o = 2
createPropellant(h2o,meth,adn)
temp = CEA_Obj(propName="WaterMethanolADN_Mix")

""" investigate falling chamber pressure """
chamber_pressure = np.linspace(0,16,1000)
chamber_pressure = chamber_pressure[1:]
expansion_ratio = 60
throat_area = 6.96e-6 #m^2
results = []

for pc in chamber_pressure:
	(isp,cstr,tc) = temp.getFrozen_IvacCstrTc(Pc=bar2psi(pc),eps=expansion_ratio,frozenAtThroat=1)
	tc  /= 1.8 # rankine to kelvin
	thrust = isp * 9.81 * pc * 1e5 * throat_area / (cstr*0.3048)
	results.append((pc,isp,tc,cstr,thrust))
	print(pc,isp)

results = np.vstack(results)



""" plot """
plt.figure()
plt.plot(results[:,0],results[:,4])
plt.xlabel('Chamber Pressure [bar]')
plt.ylabel('Thrust [N]')
plt.subplots_adjust(left=0.2)
plt.grid()
plt.savefig('b5/thrust_vs_pc.pdf')


