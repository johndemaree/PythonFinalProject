# PythonFinalProject

Date:  May 8, 2019
Project Name:  StudyCards
Project Status:  Prototype - Basic Funcionality
Project Creator:  John Demaree


Installing:

	venv -  I have created my package within a venv 

	Libraries & Dependencies using pip install

	flask  		-  webserver app
	wt_forms	- forms manager 
	flask_wtf 	- interface between flask and wt_forms
	flask_sqlalchemy- database manager with specific methods for flask
	Flask-Session	- manages session global variables


	Package
	within your install folder paste 
	run.py 		- app program
	studycards 	- package folder

Running:

	Navagate to installation Folder
	(Start venv if applicable)
	Enter:Python run.py
	Open broswer tab:
	Enter: localhost:5000/

Instructions: 

	Create a new Set of Cards:
		1.  Go to the home page  localhost:5000/
		2.  Click on "Create New Cardset"
		3.  Enter the Title and Description of the new Cardset
		4.  Click on "Create New Cardset"

	Select a Cardset:
		1.  Go to the home page  localhost:5000/
		2.  Use the drop down menu to select a Cardset
		3.  Click on "Select Cardset"
		
	Add Cards to Cardset:
		1.  Follow the instructions above for Selecting a Cardset
		2.  Click on "Add a New Card"
		3.  Enter the Key1, Key2, and Definition of the new Card.
		4.  Click "Add Another Card"  to add that card and then create a new card.
		5.  Click "Finish" to add final Card and return to Card Menu. 

	Review Cards
		1.  Follow the instructions above for Selecting a Cardset
		2.  Click on "Review Cards"  
		3.  Use the "Previous Card" and "Next Card" to Clycle through the Cards 
		4.  Note:  The card number you are viewing is displayed to the top right of the Card. 


Structure:
	run.py			- __main__ application file

	Package: studycards

	Modules
		__ini__.py  	- Initial package file
		forms.py	- Contains template forms used to create forms within the html templates
		models.py	- Contains table definitions for the SQLAlchemy database
		routes.py	- Contains route definitions for all of the links and submit operations in the pages
	
	Templates
		layout.html	- Main html code used to create each page of the webserver
		home.html	- Index page of the website used to select a Cardset 
		about.html	- About (help) page with some instructions for operating the website. 
		cardset.html	- Contains form to create a new Set of Cards
		cardmenu.html	- Menu page to select either creating a new Card or reviewing the cards in a set of cards
		newcard.html	- Contains form to creat a new Card within a specific Set of Cards
		reviewcards.html- Displays a Set of Cards one card at a time

	Static
		main.css	- Contains css for the website


TODO Functionality:

	1.  Add options to edit/delete individual Cards and Cardsets
	2.  Clean-up / Add documentation within the code and About page.
	  
	 




