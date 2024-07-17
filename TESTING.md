## TESTING

### Purpose Of Testing

The purpose of testing is to make sure the application does not have critical errors and works properly, providing a positive experience for the user.

__Functional Testing__

The all options were tested and works correctly.

| feature | action | expected result | tested | passed | comments |
| --- | --- | --- | --- | --- | --- |
| The Main Menu | | | | | |
| Start the application  | Start the application | The application displays the Welcome message and the Main Menu | Yes | Yes | - |
| The option "Authors" | Input 1 to select the option | The system dysplays the Authors' menu to work with authors | Yes | Yes | - |
| The option "Books" | Input 2 to select the option | The system dysplays the Books' menu to work with aubooksthors | Yes | Yes | - |
| The option "Exit" | Input 3 to select the option | The system exits the application and displays the message. | Yes | Yes | - |
| The Authors' Menu | | | | | |
| Dysplay the Authors' Menu  | Dysplay the Authors' Menu | The Authors' menu has five options. | Yes | Yes | - |
| The option "Get all authors" | Input 1 to select the option | The system goes to the next step | Yes | Yes | - |
| Display authors | Displays all saved authors | Displays all saved authors. The data is displayed in the format "ID (author) - the full name - the birth year" | Yes | Yes | - |
| The option "Add a new author" | Input 2 to select the option | The system goes to the next step | Yes | Yes | - |
| Input the full name of the author  | Input the full name of the author | The user can input the full name of the author. The user can input "Exit" to return to the Authors' menu. The system checks that it cannot be empty.  | Yes | Yes | - |
| Input the birth year of the author | Input the birth year of the author | The user can input the birth year of the author. The user can input "Exit" to return to the Authors' menu. The system checks that it cannot be empty and has to be an integer.  | Yes | Yes | - |
| Checks the database for duplicates | Input the data that is in the database | The system checks the database for duplicates and if it is, sends the message with the ID of an existing item. | Yes | Yes | - |
| Save the author in the database | Input the data that is not in the database | The system saves information and sends the message with details. | Yes | Yes | - |
| The option "Edit an author" | Input 3 to select the option | The system goes to the next step | Yes | Yes | - |
| Input the full name of the author or the ID of the author  | Input the full name of the author or the ID of the author | The user can input the full name of the author or the ID of the author. The user can input "Exit" to return to the Authors' menu. The system checks that it cannot be empty, finds the author and sends the result's message.  | Yes | Yes | - |
| Input the part of the full name of the author | Input the part of the full name of the author | The user can input the part of full name of the author. The user can input "Exit" to return to the Authors' menu. The system checks that it cannot be empty, finds the author and sends the result's message. The selection occurs based on the occurrence of a string. If it finds several items, the system asks the user to choose one of them.  | Yes | Yes | - |
| Input the new full name of the author | Input the new full name of the author | The user can input the new full name of the author or the ID of the author. The user can input "Exit" to return to the Authors' menu. The user can input empty string not to change the full name. | Yes | Yes | - |
| Input the birth year of the author | Input the birth year of the author | The user can input the birth year of the author. The user can input "Exit" to return to the Authors' menu. The system checks that it cannot be empty and has to be an integer.  | Yes | Yes | - |
| Save the author in the database | Input the data that is not in the database | The system saves information and sends the message with details. | Yes | Yes | - |
| The option "Find books by an author" | Input 4 to select the option | The system goes to the next step | Yes | Yes | - |
| Input the full name of the author or the ID of the author  | Input the full name of the author or the ID of the author | The user can input the full name of the author or the ID of the author. The user can input "Exit" to return to the Authors' menu. The system checks that it cannot be empty, finds the author and sends the result's message.  | Yes | Yes | - |
| Input the part of the full name of the author | Input the part of the full name of the author | The user can input the part of full name of the author. The user can input "Exit" to return to the Authors' menu. The system checks that it cannot be empty, finds the author and sends the result's message. The selection occurs based on the occurrence of a string. If it finds several items, the system asks the user to choose one of them.  | Yes | Yes | - |
| Displays books | Displays books | The system displays books in the format "ID (book) - the title - the full name of the author - shelf(the number of the shelf on which the book is stored)".  | Yes | Yes | - |
| The option "Back to the previous step" | Input 5 to select the option | The system returns to the Main menu | Yes | Yes | - |
| The Books' Menu | | | | | |
| Dysplay the Books' Menu  | Dysplay the Books' Menu | The Books' menu has five options. | Yes | Yes | - |
| The option "Get all books" | Input 1 to select the option | The system goes to the next step | Yes | Yes | - |
| Display books  | Displays all saved books | Displays all saved books. The data is displayed in the format "ID (book) - the title - the full name of the author - shelf(the number of the shelf on which the book is stored)" | Yes | Yes | - |
| The option "Add a new book" | Input 2 to select the option | The system goes to the next step | Yes | Yes | - |
| Input the full name of the author or the ID of the author  | Input the full name of the author or the ID of the author | The user can input the full name of the author or the ID of the author. The user can input "Exit" to return to the Books' menu. The system checks that it cannot be empty, finds the author and sends the result's message.  | Yes | Yes | - |
| Input the part of the full name of the author | Input the part of the full name of the author | The user can input the part of full name of the author. The user can input "Exit" to return to the Books' menu. The system checks that it cannot be empty, finds the author and sends the result's message. The selection occurs based on the occurrence of a string. If it finds several items, the system asks the user to choose one of them.  | Yes | Yes | - |
| Input the title of the books  | Input the title of the book | The user can input the title of the book. The user can input "Exit" to return to the Books menu. The system checks that it cannot be empty.  | Yes | Yes | - |
| Input the number of the shelf on which the book is stored | Input the number of the shelf on which the book is stored | The user can input the the number of the shelf on which the book is stored. The user can input "Exit" to return to the Books' menu. The system checks that it cannot be empty and has to be an integer.  | Yes | Yes | - |
| Checks the database for duplicates | Input the data that is in the database | The system checks the database for duplicates and if it is, sends the message with the ID of an existing item. | Yes | Yes | - |
| Save the book in the database | Input the data that is not in the database | The system saves information and sends the message with details. | Yes | Yes | - |
| The option "Edit a new book" | Input 3 to select the option | The system goes to the next step | Yes | Yes | - |
| Input the full name of the author or the ID of the author  | Input the full name of the author or the ID of the author | The user can input the full name of the author or the ID of the author. The user can input "Exit" to return to the Books' menu. The system checks that it cannot be empty, finds the author and sends the result's message.  | Yes | Yes | - |
| Input the part of the full name of the author | Input the part of the full name of the author | The user can input the part of full name of the author. The user can input "Exit" to return to the Books' menu. The system checks that it cannot be empty, finds the author and sends the result's message. The selection occurs based on the occurrence of a string. If it finds several items, the system asks the user to choose one of them.  | Yes | Yes | - |
| Input the title of the book or the ID of the book  | Input the title of the book or the ID of the book | The user can input the title of the book or the ID of the book. The user can input "Exit" to return to the Books' menu. The system checks that it cannot be empty, finds the book and sends the result's message.  | Yes | Yes | - |
| Input the part of the title of the book | Input the part of the title of the book | The user can input the part of title of the book. The user can input "Exit" to return to the Books' menu. The system checks that it cannot be empty, finds the book and sends the result's message. The selection occurs based on the occurrence of a string. If it finds several items, the system asks the user to choose one of them.  | Yes | Yes | - |
| Input the new title of the books  | Input the new title of the book | The user can input the new title of the book. The user can input "Exit" to return to the Books menu. The user can input empty string not to change the title.  | Yes | Yes | - |
| Input the new number of the shelf on which the book is stored | Input the new number of the shelf on which the book is stored | The user can input the the new number of the shelf on which the book is stored. The user can input "Exit" to return to the Books' menu. The system checks that it cannot be empty and has to be an integer.  | Yes | Yes | - |
| Save the book in the database | Input the data that is not in the database | The system saves information and sends the message with details. | Yes | Yes | - |
| The option "Find books by part of the title" | Input 4 to select the option | The system goes to the next step | Yes | Yes | - |
| Input the part of the title of the book | Input the part of the title of the book | The user can input the part of the title of the book. The user can input "Exit" to return to the Books' menu. | Yes | Yes | - |
| Displays books | Displays books | The system displays books in the format "ID (book) - the title - the full name of the author - shelf(the number of the shelf on which the book is stored)".  | Yes | Yes | - |
| The option "Back to the previous step" | Input 5 to select the option | The system returns to the Main menu | Yes | Yes | - |