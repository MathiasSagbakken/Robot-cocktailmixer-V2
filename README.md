

# Robot-cocktailmixer-V2


A robot cocktail mixer which mixes drinks based on user input. A drink is chosen by pressing the picture of the spescific cocktail in the recycleview on the touchscreen. After having accepted your doom, the robot will go to all the diffent ingredients for the specific cocktail and pour the correct volume. The time it takes to make one drink varies by the amount of liquid, but is most often between 30 and 60 seconds. 



<p align="center">
<img src="https://github.com/MathiasSagbakken/Robot-cocktailmixer-V2/blob/master/robot_image1.jpg" alt="robot_cocktailmixer"
	title="Front view of the robot" width="400" height="600" />
</p>

# How to run the software

* Requires kivy 2.0

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




