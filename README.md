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
![The Books' Menu](documentation/features/authors-menu.png)
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

