from os.path import expanduser
home = expanduser("~")
from specIO import *
from flask import render_template,Flask, jsonify
import numpy as np
from scipy import interpolate
import pandas as pd
import matplotlib,os

def wavelength_to_rgb(wavelength, gamma=0.8):

    '''This converts a given wavelength of light to an 
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 700:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
            
    else:
        R = .0
        G = .0
        B = .0
        #B = blue[int(wavelength)]

    return R,G,B

#get spectrometer make
spectrometer = 0
while spectrometer not in  ['ASD', 'SVC', 'SE']:
    spectrometer = raw_input('Spectrometer (ASD, SVC, SE):   ')
spectrometer = "SE"

#get data directory
data_dir = '0'
while not os.path.isdir(data_dir):
    data_dir = raw_input('Spectral file output directory:   ')

#data directory
data_dir = "%s/Dropbox/projects/mannrs/data/" % home

#load water absorption feature colors
blue =  pd.read_csv("%s/Dropbox/projects/specGUI/data/water_absorption_blues.csv" % home,index_col = 0 ).T

#list of file extensions
file_ext  = {"ASD":".asd","SVC":".sig", "SE":".sed"}

#get number of file in output directory
num_files = len([x for x in os.listdir(data_dir) if x.endswith(file_ext[spectrometer])])


def process_spectrum(index,sampling_interval):
    
    #get list of spectra
    spectral_list = [x for x in os.listdir(data_dir) if x.endswith(file_ext[spectrometer])]
    
    #update index if out of range
    if index >= len(spectral_list):
        index = len(spectral_list) -1
    elif index < 0:
        index= 0
    
    #load data
    spectrum = openSE(data_dir+spectral_list[index])

    #process data
    spectrum.refl  = 1000* (spectrum.refl/ np.linalg.norm(spectrum.refl))
    spectrum.refl = spectrum.refl.loc[range(400,2501,1)]
    spectrum.refl.name = "value"    
    bins = np.digitize(spectrum.refl.index,range(400,2500,sampling_interval))    
    spectrum = spectrum.refl.groupby(by = bins)    
        
    #weight the wavelength colors by the reflectance magnitude
    colors = []
    
    for ix,spec_bin in spectrum:
        color = matplotlib.colors.rgb2hex(wavelength_to_rgb((spec_bin.index *(spec_bin/spec_bin.sum())).values.sum()))    
        colors.append(color)
    
    waves = [np.ceil(np.mean(x[1].index)) for x in spectrum]   
    spect_sum = spectrum.sum()
    spectrum = spectrum.mean()
    spectrum.index= waves
    
    spect = pd.DataFrame()
    spect["value"] = spectrum
    spect["color"] =colors
    
    
    #convert spectrum data to json and add to dictionary
    data_dict = {}
    data_dict["data"] = spect.to_json(orient = "index")
    data_dict["index"] = index
    
    return spect.to_json(orient = "index")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_data/<event_type>")
def send_data(event_type):
    
    index, sampling_interval = event_type.split("_")
    return process_spectrum(int(index), int(sampling_interval))

@app.route("/new_data")
def new_data():
    
    data_dict = {}
    
    global num_files
    
    if len([x for x in os.listdir(data_dir) if x.endswith("sed")]) > num_files:
        new_data_state = 1
        num_files = len([x for x in os.listdir(data_dir) if x.endswith("sed")])
        
    else:
        new_data_state=0
    
    data_dict["new"] = new_data_state
    data_dict["index"] = num_files-1
    print data_dict
    
    return  jsonify(data_dict)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
    
    
    
    
    