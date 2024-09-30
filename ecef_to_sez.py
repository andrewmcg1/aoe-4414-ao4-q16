# script_name.py
#
# Usage: python3 eci_to_ecef.py arg1 arg2 ...
#  Text explaining script usage
# Parameters:
#  arg1: description of argument 1
#  arg2: description of argument 2
#  ...
# Output:
#  A description of the script output
#
# Written by Andrew McGrellis
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
import math # math module
import sys # argv
import numpy as np

# "constants"
R_E_KM  = 6378.1363
EE_E    = 0.081819221456
W       = 7.292115e-5

# helper functions


## function description
def calc_denom(ecc, lat_rad):
  return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad)**2))

# initialize script arguments
# arg1 = '' # description of argument 1
# arg2 = '' # description of argument 2

# parse script arguments
if len(sys.argv) == 7:
    o_x_km = float(sys.argv[1])
    o_y_km = float(sys.argv[2])
    o_z_km = float(sys.argv[3])
    x_km = float(sys.argv[4])
    y_km = float(sys.argv[5])
    z_km = float(sys.argv[6])
else:
  print(\
   'Usage: '\
   'python3 arg1 arg2 ...'\
  )
  exit()

# write script below this line

lon_rad = math.atan2(o_y_km,o_x_km)
lon_deg = lon_rad*180.0/math.pi

# initialize lat_rad, r_lon_km, r_z_km
lat_rad = math.asin(o_z_km/math.sqrt(o_x_km**2+o_y_km**2+o_z_km**2))
r_lon_km = math.sqrt(o_x_km**2+o_y_km**2)
prev_lat_rad = float('nan')

# iteratively find latitude
c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
  denom = calc_denom(EE_E,lat_rad)
  c_E = R_E_KM/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((o_z_km+c_E*(EE_E**2)*math.sin(lat_rad))/r_lon_km)
  count = count+1
  
# calculate hae
hae_km = r_lon_km/math.cos(lat_rad)-c_E

R = [[-math.sin(lon_rad), math.cos(lon_rad), 0],
     [-math.sin(lat_rad)*math.cos(lon_rad), -math.sin(lat_rad)*math.sin(lon_rad), math.cos(lat_rad)],
     [math.cos(lat_rad)*math.cos(lon_rad), math.cos(lat_rad)*math.sin(lon_rad), math.sin(lat_rad)]]

enu = np.dot(R, [[x_km], [y_km], [z_km]])
sez = [[-enu[1][0]], [enu[0][0]], [enu[2][0]]]

print(sez[0][0])
print(sez[1][0])
print(sez[2][0])