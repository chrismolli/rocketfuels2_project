from rocketcea.cea_obj import CEA_Obj, add_new_propellant

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

""" get full output """
chamber_pressure = 16
expansion_ratio = 60

temp = CEA_Obj(propName="WaterMethanolADN_Mix")
(isp,cstr,tc) = temp.getFrozen_IvacCstrTc(Pc=bar2psi(chamber_pressure),eps=expansion_ratio,frozenAtThroat=1)
print(isp,cstr,tc)
s = temp.get_full_cea_output( Pc=bar2psi(chamber_pressure), eps=expansion_ratio, frozen=1, frozenAtThroat=1)
with open("b4.out","w") as f:
	f.write(s)
print(s)