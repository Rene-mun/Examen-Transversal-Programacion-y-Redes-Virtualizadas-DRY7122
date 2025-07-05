vlan=int(input("Ingrese el número de la VLAN: "))
if vlan>=1 and vlan<=1005:
    print("La vlan ",vlan, "es de rango normal.")
elif vlan>=1006 and vlan<=4094:
    print("La vlan ",vlan, "es de rango extendido.")
else:
    print("La vlan ",vlan, "no es un número válido.")