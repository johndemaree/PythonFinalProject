# PythonFinalProject

Date:  May 28, 2019
Project Name:  StudyCards
Project Status:  Final Project - Full Funcionality
Project Creator:  John Demaree


Installing:
	python - This program was written using Python 3.7.2
	venv -  I have created my package within the optional virtual environment venv 

	Libraries & Dependencies using pip install

	flask  		-  webserver app
	wt_forms	- forms manager 
	flask_wtf 	- interface between flask and wt_forms
	flask_sqlalchemy- database manager with specific methods for flask
	Flask-Session	- manages session global variables
	PILLOW		- library of tools for image manipulation


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
		1.  Browse to the home page  localhost:5000/
		2.  Click on "Create New Cardset"
		3.  Enter the Title and Description of the new Cardset
		4.  Click on "Create New Cardset"

	Select a Cardset:
		1.  Browse to the home page  localhost:5000/
		2.  Use the drop down menu to select a Cardset
		3.  Click on "Select Cardset"
		
	Edit a Cardset:
		1.  Browse to the home page localhost:5000/
		2.  Use the drop down menu to select a Cardset
                3.  Click on  "Edit CardSet"

	Add Cards to Cardset:
		1.  Follow the instructions above for Select a Cardset
		2.  Click on "Add a New Card"
		3.  Enter the Key1, Key2, and Definition of the new Card.
		4.  Click "Add Another Card"  to add that card and then create a new card.
		5.  Click "Finish" to add final Card and return to Card Menu. 

	Review Cards
		1.  Follow the instructions above for Select a Cardset
		2.  Click on "Review Cards"  
		3.  Use the "Previous Card" and "Next Card" to Clycle through the Cards 
		4.  Note:  The card number you are viewing is displayed to the top right of the Card. 
	Edit/Delet Cards
		1.  Follow the instructions above for Review Cards
		2.  Select the Card you want to edit or delete
		3.  Click on "Edit"  to open the card in an editable form
		4.  Click on "Finish" after you have made changes to save those changes
		5.  Clock on "Delete"  to delete the current card.
	Flash Cards
		1.  Follow the instructions above for Selecting a Cardset
		2.  Click on "Flash Cards"
		3.  Use the form to select which items will appear on the Front of the Card and then the Back.
		Note:  You can select items to appear on both front and back, or neither front or back.  
		4.  Click on "Submit"  The cards will be sorted in a random order and the Front of the first card will appear. 
		5.  Click on "Back"  to reveal the back of the card.
		6.  Click on "Next"  to reveal the front of the next card. 




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
		editcard.html	- Contains form to edit or delete a specific card within a specific Set of Cards
		flashform.html	- Contains form to select which items will appear on the front and back of the flash cards
		flashfront.html - Displays the front of a Flash card based on user input
		flashback.html	- Displays the back of a Flash card based on  user input

	Static
		main.css	- Contains css for the website
		images		- Folder containing images used on cards mostly uploaded by user, but inlcuding a few default images.
		flavicon.ico	- File contains image used by browers next to title on tab.

