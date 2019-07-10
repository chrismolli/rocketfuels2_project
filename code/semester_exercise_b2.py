from rocketcea.cea_obj import CEA_Obj, add_new_propellant

def kilojoule2cal(kilojoule):
	return kilojoule/4.184*1000

def bar2psi(bar):
	return bar*14.504

""" define LMP-103S propellant """
card_str = """
name H2O   H 2 O 1   wt%=14.0
h,kj/mol=-285.8     t(k)=293.15
name Ammonia   N 1 H 3   wt%=4.6
h,kj/mol=-78.46      t(k)=293.15
name Methanol   C 1 H 4 O 1   wt%=18.4
h,kj/mol=-239.2      t(k)=293.15
name ADN   H 4 N 4 O 4   wt%=63.0
h,kj/mol=-134.6       t(k)=293.15
"""
add_new_propellant("LMP103S",card_str)

""" define AF-M315E propellant """
card_str = """
name H2O   H 2 O 1   wt%=11.0
h,kj/mol=-285.8     t(k)=293.15
name HAN   H 4 N 2 O 4   wt%=44.5
h,kj/mol=-366.52      t(k)=293.15
name HEHN   C 2 H 9 N 3 O 4   wt%=44.5
h,kj/mol=-486.00      t(k)=293.15
"""
add_new_propellant("AFM315E",card_str)

""" define PeroxideWater98 propellant """
card_str = """
name H2O   H 2 O 1   wt%=2.0
h,kj/mol=-285.5     t(k)=293.15
name H2O2   H 2 O 2   wt%=98.0
h,kj/mol=-187.8       t(k)=293.15
"""
add_new_propellant("PeroxideWater98",card_str)


""" calculate combustion """
chamber_pressure = 24 #bar
expansion_ratio = 60
# no mixing ratio needed since its a pre-mixed mono propellant

# propellant = CEA_Obj(propName="AFM315E")
for propellant in ["LMP103S","AFM315E","PeroxideWater98"]:
	print("###    ###    ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###")
	for chamber_pressure in [3.67,16]:
		cea = CEA_Obj(propName=propellant)
		# print("{:20s}\tISP ".format(propellant),cea.get_Isp( Pc=bar2psi(chamber_pressure), eps=expansion_ratio))
		# print(cea.get_full_cea_output( Pc=bar2psi(chamber_pressure), eps=expansion_ratio, short_output=1, frozen=1, frozenAtThroat=1))
		(isp,cstr,tc) = cea.getFrozen_IvacCstrTc(Pc=bar2psi(chamber_pressure),eps=expansion_ratio,frozenAtThroat=1)
		tc /= 1.8 # rankine to kelvin
		print("Performance of {} @ Pc = {}bar: ISP: {:.2f}s \t Tc: {:.2f}K".format(propellant,chamber_pressure,isp,tc))
print("###    ###    ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###")
