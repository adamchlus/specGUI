# specGUI

specGUI is a web based GUI for plotting spectra in real time from a number of spectrometer
manufacturers. The idea behind it was to display spectra in a unified way across all spectrometer
brands and in a way in which non-experts (ie. high schoolers) would be able to understand the output.
It was developed as part of a lab for high school students demonstrating the optical properties of leaves.

Below is a gif of the GUI in action, visible wavelengths are colored by the color we see and blues in the
infrared are a function of water aborption, more blue = more water absorption at that wavelength.

![](https://github.com/adamchlus/specGUI/gui_example.gif)

The GUI itself is run by a local webserver and uses d3.js to display the spectra. specGUI does not
directly communicate with the spectrometer to collect data and the manufacturer software needs to be
running as well, the software is best run in a dual monitor setup with specGUI on the main/larger
screen and the manufacturer software on the secondary screen.
