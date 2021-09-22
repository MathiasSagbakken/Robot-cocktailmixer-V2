

# Robot-cocktailmixer-V2


A robot cocktail mixer which mixes drinks based on user input. A drink is chosen by pressing the picture of the spescific cocktail in the recycleview on the touchscreen. After having accepted your doom, the robot will go to all the diffent ingredients for the specific cocktail and pour the correct volume. The time it takes to make one drink varies by the amount of liquid, but is most often between 30 and 60 seconds. 



<p align="center">
<img src="https://github.com/MathiasSagbakken/Robot-cocktailmixer-V2/blob/master/robot_image1.jpg" alt="robot_cocktailmixer"
	title="Front view of the robot" width="400" height="600" />
</p>

# How to run the software

The python (GUI) part only requires Kivy gui, and Serial which can easly be obtained with pip install. Easiest way of making kivy work is to install it with conda.

* Requires kivy 2.0	(conda install kivy -c conda-forge)
* Requires serial	(pip install serial)
* Upload arduino code to arduino of your choosing

note: The GUI is coded in a way that it requires to be connected to an arduino so that it has a serial connection to start. This is commented out in the code, so this will not be a problem if you only want to boot up the GUI without having to deal with an arduino. As stated in the kivy install guide, its recomended to install kivy in a virtual enviroment.

<p align="center">
<img src="https://github.com/MathiasSagbakken/Robot-cocktailmixer-V2/blob/master/robot_gif1.gif" alt="robot_cocktailmixer"
	title="Front view of the robot" width="800" height="450" />
</p>


# Motivation and solution to problem

As a student of robotics and artificial intelligence I enjoy creating projects on the side wich introduces physical and virtual problems that is not always so common in the academia side of my studies. I saw examples of these types of robots and thought it would make a great project. This project was very much made from scratch starting with planning the design of the robot and then implementation of code.

I wanted to make the software side convenient and easy to use. Therefore all one needs to use the robot is to hook up bottles to dispensers and type in the Ingrdients. The program will then cross refference the ingredients to recepies of all cocktails in the database (json file containing around 600 different cocktails) and if all the ingredients of a cocktail is in the user-inputted ingredient list, there is a match and the cocktail will be displayed in the GUI on the touchscreen. The cocktails in the database is taken from an open source database called "thecocktaildb". The program also lets the user input custom cocktails or remove them. 


<p align="center">
<img src="https://github.com/MathiasSagbakken/Robot-cocktailmixer-V2/blob/master/robot_image2.jpg" alt="robot_cocktailmixer"
	title="Front view of the robot" width="400" height="600" />
</p>

# Features
* Touchscreen control
* A fast and easy to use graphical user interface. 
* All recepies are stored in a readable JSON file and the majority of cocktails comes from an open source cocktail api called thecocktaildb. This way all the user needs to do is to input ingredients one intends to use and all possibe cocktails will be displayed.
* Option to add a cocktail to the JSON file through the GUI on the touchscreen
* Option to remove a cocktail in the JSON file through the GUI on the touchscreen
* 8 dispensers, therefore support for 8 different ingredients 


# Parts list

necessary parts that I used for this project:

Main construction:
* Coffe table 100cm*45cm*50cm
* A metal plate (brass) with dimensions 100cm*50cm
* 8 bar optics 25ml
* 2 aluminium racks for the bar optics
* 1 aluminium profile V-Slot 2060
* M8 screws
* M8 spacers

Electronics:
* power supply of 12 volt
* 2 A4988 stepper motor driver
* 1 arduini nano
* Power cable for arduino nano
* Raspberry pi 3b+
* Power cable for raspberry pi
* 2 NEMA 17 stepper motors of medium size (Y-axis motor has to have about 1 miliamp from the stepperdriver or it wont have enough tourqe to activate dispensers)
* Official raspberry pi touchscreen
* 2 limit switches
* 2 5k ohm ressistance
* 2 50v capacitors
* female to female wires
* male to female wires
* male to male wires
* 10m 0.75mm^2 copper wires

Carriage:
* 1 timing pulley 30 tooth
* 1.3m timing belt 2GT
* Aluminium spacers
* Ratrig Delrin Wheels for aluminiumprofile
* 2 Aluminium buildplates
* 1 Anti-Backlash Nut Block for 8mm Metric Acme Lead Screw
* 1 25cm 8mm lead screw
* 1 aluminium 50cm 8mm rod
* 1 5mm* 8mm Flexible Coupling  
* M5 screws
* M3 screws
