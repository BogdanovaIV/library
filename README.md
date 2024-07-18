# Library Data Automation

Library Data Automation is a Python terminal application used to store information about authors and books. It allows the user to get the list of authors and books, add a new author and a new book, edit existing authors and books and display books with a section by an author and a part of the title.

The application can be accessed through this [link](https://library2024-806c35817f2e.herokuapp.com/)

![Responsive Mockup](documentation/library-mockup.png)

## User Stories

__First Time Visitors To The Application__

 - As a new visitor, I want to quickly understand how to use this application.
 - As a new visitor, I want to get a convenient menu to manage this application.
 - As a new visitor, I want to get features allowing to add, edit and get information about authors and books.

__Returning Or Regular Visitors__

 - As a returning or regular user, I want to get saved information about authors and books.
 - As a returning or regular user, I want to have the feature editing saved information.

## Features

### Existing Features

__Start The Application__

The application displays the Welcome message and the Main Menu.
 ![Start the application](documentation/features/start-application.png)

__The Main Menu__

The Main menu has three options:
- 1. Authors - open the Authors menu to work with authors.
- 2. Books - open the Books menu to work with books.
- 3. Exit - exits the application and displays the message.
    ![Exit the application](documentation/features/exit-application.png)

__The Authors' Menu__

The Authors' menu has five options.
![The Authors Menu](documentation/features/authors-menu.png)
To choose one of the options, the user has to input the number of the option and press Enter.
- 1. Get all authors - displays all saved authors. The data is displayed in the format "ID (author) - the full name - the birth year"
     ![Get all authors](documentation/features/get-all-authors.png)
- 2. Add a new author - add a new author to the database.
     - The system asks the user to input the full name of the author and checks that it cannot 
     be empty. The user can input "Exit" to return to the Authors' menu.
     ![Input the full name](documentation/features/input-full-name.png)
     - Then the system asks the user to input the birth year of the author and checks that it cannot be empty and has to be an integer. The user can input "Exit" to return to the Authors' menu.
     ![Input the birth year](documentation/features/input-birth-year.png)
     - Then the system checks the database for duplicates and if it is, sends the message.
     ![The duplicate message](documentation/features/duplicate-author.png)
     Finally, the system saves information and sends the message with details.
     ![The saved message](documentation/features/save-author.png)
- 3. Edit an author - edit detailed information about the chosen author.
     - The system asks the user to input the full name of the author or the ID of the author, checks that it cannot be empty, finds the author and sends the result's message. The user can input "Exit" to return to the Authors' menu.
     ![The Message of Found Author](documentation/features/find-author-by-id-or-full-name.png)
     - The selection occurs based on the occurrence of a string. If it finds several items, the system asks the user to choose one of them.
     ![Choose the author](documentation/features/choose-author.png)
     - Then the system asks the user to input the new full name of the author. The user can input an empty string not to change the full name or "Exit" to return to the Authors' menu.
     - Then the system asks the user to input the new birth year of the author and checks that it cannot be empty and has to be an integer. The user can input "Exit" to return to the Authors' menu.
     - Finally, the system saves information and sends the message with details.
     ![The saved message](documentation/features/update-author.png)
- 4. Find books by an author - displays books with the selection by the author.
     - The system asks the user to input the full name of the author or the ID of the author, checks that it cannot be empty, finds the author and sends the result's message. The user can input "Exit" to return to the Authors' menu. The selection occurs based on the occurrence of a string. If it finds several items, the system asks the user to choose one of them.
     - Then the system displays books in the format "ID (book) - the title - the full name of the author - shelf(the number of the shelf on which the book is stored)".
     ![The list of books](documentation/features/list-books-selected-by-author.png)
- 5. Back to the previous step - return to the Main menu.

__The Books' Menu__

The Books' menu has five options.
![The Books' Menu](documentation/features/books-menu.png)
To choose one of the options, the user has to input the number of the option and press Enter.
- 1. Get all books - displays all saved books. The data is displayed in the format "ID (book) - the title - the full name of the author - shelf(the number of the shelf on which the book is stored)"
     ![Get all books](documentation/features/get-all-books.png)
- 2. Add a new book - add a new book to the database.
     ![Add a new book](documentation/features/add-new-book.png)
     - The system asks the user to input the full name of the author or the ID of the author, checks that it cannot be empty, finds the author and sends the result's message. The user can input "Exit" to return to the Books' menu. The selection occurs based on the occurrence of a string. If it finds several items, the system asks the user to choose one of them.
     - Then The system asks the user to input the title and checks that it cannot 
     be empty. The user can input "Exit" to return to the Books' menu.
     - Then The system asks the user to input the the number of the shelf on which the book is stored and checks that it cannot be empty. The user can input "Exit" to return to the Books' menu.
     - Then the system checks the database for duplicates and if it is, sends the message.
     ![The duplicate message](documentation/features/duplicate-book.png)
     - Finally, the system saves information and sends the message with details.
     ![The saved message](documentation/features/save-book.png)
- 3. Edit a book - edit detailed information about the chosen book.
     - The system asks the user to input the full name of the author or the ID of the author, checks that it cannot be empty, finds the author and sends the result's message. The user can input "Exit" to return to the Books' menu. The selection occurs based on the occurrence of a string. If it finds several items, the system asks the user to choose one of them.
     - Then the system asks the user to input the title of the book or ID of the book and checks that it cannot be empty. The user can input "Exit" to return to the Books' menu.
     - Then the system finds the book and sends the result's message.
     ![The found message](documentation/features/find-book-by-id-or-full-name.png) 
     - Then the system asks the user to input the new title of the book. The user can input an empty string not to change the title or "Exit" to return to the Books' menu.
     - Then The system asks the user to input the the number of the shelf on which the book is stored and checks that it cannot be empty. The user can input "Exit" to return to the Books' menu.
     - Finally, the system saves information and sends the message with details.
     ![The saved message](documentation/features/update-book.png)
- 4. Find books by part of the title - displays books based on the occurrence of a string.
     - The system asks the user to input the title.
     - Then the system finds books by part of the title.
     ![The found books](documentation/features/find-books-by-title.png)
- 5. Back to the previous step - return to the Main menu.

## Technologies Used

### Programming Language
- [Python 3.12.2](https://www.python.org/downloads/release/python-3122/): A versatile and widely-used programming language known for its readability and extensive libraries. This project is primarily built using Python due to its powerful data manipulation capabilities and ease of integration with other technologies.

### Libraries and Frameworks
- [gspread](https://docs.gspread.org/en/v6.0.0/): A Python library that provides easy access to Google Sheets API. It allows for seamless reading, writing, and updating of Google Sheets.
- [google-auth](https://google-auth.readthedocs.io/en/master/): A library to authenticate and authorize Google APIs. Specifically, google.oauth2.service_account is used to handle service account credentials for secure access to Google Sheets.
- [uuid](https://docs.python.org/3/library/uuid.html): A Python library used to generate unique identifiers for records, ensuring that each entry in the Google Sheets has a unique ID.
- [colorama](https://pypi.org/project/colorama/): A library for colored terminal text, enhancing the user interface for command-line interactions.
- [simple_term_menu](https://pypi.org/project/simple-term-menu/): A library for creating simple and interactive terminal menus, improving the command-line user experience.
- [tabulate](https://pypi.org/project/tabulate/): A Python library used to format tabular data in plain text, providing an easy way to display data in a structured format.

### Google Cloud Platform
- [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python?hl=en): An API provided by Google that allows interaction with Google Sheets. This project leverages the API to read, write, and manage data stored in Google Sheets.
- [Google Drive API](https://developers.google.com/drive/api/quickstart/python?hl=en): Used for additional operations related to file management in Google Drive, complementing the Google Sheets API functionalities.

### Google Cloud Platform
- [VS Code](https://code.visualstudio.com/): Popular Integrated Development Environments (IDEs) that provide robust support for Python development, including code completion, debugging, and version control integration.
- [Github](https://github.com/) - A version control system used to manage code changes and collaborate with other developers.

### Authentication and Security
- [OAuth 2.0](https://oauth.net/2/): An authorization framework used to obtain limited access to user accounts on an HTTP service. This project uses OAuth 2.0 to securely access Google Sheets data through a service account.

### Data Formats
- [JSON](https://www.json.org/json-en.html): Used for configuration and data exchange. The credentials for the Google service account are stored in a JSON file, and JSON is also used for structured data interchange.

### Object-Oriented Programming
Object-Oriented Programming (OOP) is a programming paradigm that uses objects and classes to structure software in a way that is both modular and reusable. 

#### Classes Used in This Project
- GoogleSheetsClient - A client class to handle authentication and connection to Google Sheets.
- GoogleSheet - A class to handle operations on a specific Google Sheet worksheet.
- UniqueIDMixin - A mixin class that generates unique IDs.
- InputMixin - A mixin class that calls input which checks the value.
- Menu - A class representing a menu-driven interface.
- Author - A class representing an individual author.
- Authors - A class managing a collection of authors in a Google Sheets document.
- Book - A class representing a book.
- Books - A class managing a collection of books in a Google Sheets document.

## Testing

Please refer to the [TESTING.md](TESTING.md) file for all test-related documentation.

## Deployment
The application was deployed to Heroku using the web interface. 
The live link can be found [here](https://library2024-806c35817f2e.herokuapp.com/)
The steps to deploy are as follows:
- 1. Login to Heroku
     Go to [Heroku](https://dashboard.heroku.com/) and log in to your account. If you don't have an account, you can sign up for free.
- 2. Create a New Application
     - Click on the "New" button in the top right corner of the dashboard.
     - Select "Create new app" from the dropdown menu.
     - Enter a name for your app and select your region.
     - Click the "Create app" button.
     ![Heroku - create a new application](documentation/heroku/heroku-create-app.png)
- 3. Set Up Environment Variables
     - Go to the "Settings" tab of your Heroku app.
     - Click "Reveal Config Vars".
     - Add any necessary environment variables: CREDS equal JSON and PORT equal 8000
      ![Heroku - config var](documentation/heroku/heroku-config-var.png)
- 4. Buildpacks
     - Click "Add buildpack"
     - Chose python and nodejs
     ![Heroku - buildpacks](documentation/heroku/heroku-buildpacks.png)
- 5. Connect to GitHub
     - In the "Deploy" tab, go to the "Deployment method" section.
     - Click on the "GitHub" button to connect your GitHub account to Heroku.
     - Once connected, search for the repository you want to deploy.
     - Click the "Connect" button next to your repository.
     ![Heroku - github](documentation/heroku/heroku-github.png)
- 6. Automatic Deploys (Optional)
     - In the "Automatic deploys" section, you can enable automatic deploys for a specific branch (typically main or master).
     - Click "Enable Automatic Deploys" if you want Heroku to automatically deploy every time you push changes to the specified branch.
     ![Heroku - automatic deploys](documentation/heroku/heroku-automatic-deploys.png)
- 7. Manual Deploy
     - In the "Manual deploy" section, select the branch you want to deploy and click "Deploy Branch".
     - Heroku will start the deployment process. You can view the build progress in the activity feed.
     ![Heroku - manual deploys](documentation/heroku/heroku-manual-deploys.png)

## Local Deployment

### Prerequisites
Before running the application locally, ensure you have the following installed:
- Python (preferably the latest version, check the version with python --version).
- pip (Python package installer, included with Python installations).
- Git (for cloning the repository).
### Steps to Deploy Locally
- Clone the Repository
  git clone https://github.com/BogdanovaIV/library.git
  cd library
- Create the creds.json File. Ensure you have the creds.json file, which contains your Google API credentials. Place the creds.json in the project directory
- Install Dependencies. Install the required packages listed in the requirements.txt file:
  pip install -r requirements.txt
- Run the Application. Run your main application script.
  python run.py

## Future Improvements

- Delete items from the database.
- Save information about people who take the book.
- Add more detailed information about books like descriptions, reviews, etc.

## Credits 

### Content 

- Information about authors and books was taken from free sources like Wikipedia
- ![Love Sandwiches](https://github.com/Code-Institute-Solutions/love-sandwiches-p5-sourcecode/tree/master/05-deployment/01-deployment-part-1) is a tutorial project that covers the general principles of writing code and deploying it.

### Acknowledgments

- [Juliia Konovalova](https://github.com/IuliiaKonovalova/) was a great mentor who helped me to reveal my abilities and gave valuable advice.
- [Code Institute team](https://codeinstitute.net/) supported me and provided all the information that I needed.
- [Github](https://github.com/) provided free access to a versioning system.
- [Heroku](heroku.com) provided a service to deploy an application.
- [gspread](https://docs.gspread.org/en/v6.0.0/) is a free Python library that provides easy access to Google Sheets API. It allows for seamless reading, writing, and updating of Google Sheets.
- [google-auth](https://google-auth.readthedocs.io/en/master/) is a free library to authenticate and authorize Google APIs. Specifically, google.oauth2.service_account is used to handle service account credentials for secure access to Google Sheets.
- [uuid](https://docs.python.org/3/library/uuid.html) is a free Python library used to generate unique identifiers for records, ensuring that each entry in the Google Sheets has a unique ID.
- [colorama](https://pypi.org/project/colorama/) is a free library for colored terminal text, enhancing the user interface for command-line interactions.
- [simple_term_menu](https://pypi.org/project/simple-term-menu/) is a free library for creating simple and interactive terminal menus, improving the command-line user experience.
- [tabulate](https://pypi.org/project/tabulate/) is a free Python library used to format tabular data in plain text, providing an easy way to display data in a structured format.