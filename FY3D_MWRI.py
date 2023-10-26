import os
import glob
import h5py
import numpy as np
import pandas as pd

def convert(band, intercept):
    band = band * 0.01 + intercept
    return band
    
def openfile(fname):
    file = h5py.File(fname, "r")
    if file.attrs["Satellite Name"] == "FY-3G":
        lons, lats = file["S1"]["Geolocation"]["Longitude"][:], file["S1"]["Geolocation"]["Latitude"][:]
        btds = file["S1"]["Data"]["EARTH_OBSERVE_BT_10_to_89GHz"]
    else:
        lons, lats = file["Geolocation"]["Longitude"][:], file["Geolocation"]["Latitude"][:]
        btds = file["Calibration"]["EARTH_OBSERVE_BT_10_to_89GHz"]
    btlist = ["bt_10v","bt_10h","bt_18v","bt_18h","bt_23v","bt_23h","bt_36v","bt_36h","bt_89v","bt_89h"]
    bandnum = 0
    intercept = btds.attrs["Intercept"]
    for var in btlist:
        if file.attrs["Satellite Name"] == "FY-3G":
            globals()[var] = btds[:,:,bandnum]
            bandnum += 1
        else: 
            globals()[var] = btds[bandnum]
            bandnum += 1
    for var in btlist:
        globals()[var] = convert(eval(var), intercept)

    return bt_10v, bt_10h, bt_18v, bt_18h, bt_23v, bt_23h, bt_36v, bt_36h, bt_89v, bt_89h, lons, lats


#Quick Start
fname = "C:/Users/Administrator/Desktop/FY3D_MWRIA_GBAL_L1_20210504_0514_010KM_MS.HDF"
bt_10v, bt_10h, bt_18v, bt_18h, bt_23v, bt_23h, bt_36v, bt_36h, bt_89v, bt_89h, lons, lats = openfile(fname)
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
crs = ccrs.PlateCarree()
f, ax = plt.subplots(subplot_kw=dict(projection=crs))
gl = ax.gridlines(
    crs=ccrs.PlateCarree(),
    draw_labels=False,
    linewidth=0,
    linestyle=':',
    color='w',
)
gl.rotate_labels = False
gl.xlabels_top = False
gl.xlabels_bottom = True
gl.ylabels_right = False
gl.ylabels_left = True
gl.xlabel_style = {'size': 5, 'color': 'k'}
gl.ylabel_style = {'size': 5, 'color': 'k'}
ax.set_extent([111, 117, 20, 26],crs=crs)
plt.pcolormesh(lons, lats, bt_89v, transform=crs)
cbar = plt.colorbar()
cbar.set_label(r'Brightness Temperature (K)')
