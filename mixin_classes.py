import uuid
from colorama import Fore, init


init(autoreset=True)


class UniqueIDMixin:
    """
    A mixin class that generates unique IDs.

    Methods:
        generate_unique_id: Generates a new unique ID.
    """

    @staticmethod
    def generate_unique_id():
        """
        Generates a new unique ID.

        Returns:
            str: A unique ID string.
        """
        return str(uuid.uuid4())


class InputMixin:
    """
    A mixin class that calls input which checks the value.

    Methods:
        input_int: Input the value which is an integer.
    """

    @staticmethod
    def input_int(text_message):
        """
        Input the value which is an integer.

        Args:
            text_message (str): The message is sent to the user.

        Returns:
            integer or None: The value inputted by the user.
        """
        value = None
        while True:
            try:
                # Prompt the user for input
                value = input(text_message)
                # Check if the user wants to exit
                if value.lower() == "exit":
                    # Set a value to None to exit input loop
                    value = None
                else:
                    # Convert the input to an integer
                    value = int(value)

                if value <= 0:
                    raise ValueError("Value cannot be negative")
            except ValueError as e:
                print(
                    Fore.RED +
                    f"Invalid data: it can be a positive whole number without "
                    f"spaces, please try again.\n"
                )
            else:
                # Break out of input loop if the input is valid
                break

        return value

    @staticmethod
    def input_str(
        text_message,
        empty_str_avaliable=False,
        exit_str_avaliable=False
    ):
        """
        Input the value which is a string.

        Args:
            text_message (str): The message is sent to the user.
            empty_str_avaliable (boolean): Allow to return an empty string.
            exit_str_avaliable (boolean): Allow to return a string
            equal "exit".

        Returns:
            string or None: The value inputted by the user.
        """
        value = None
        while True:
            try:
                # Prompt the user for input
                value = input(text_message).strip()
                if not empty_str_avaliable and not value:
                    # Raise error if empty string not allowed and
                    # the input is empty
                    raise ValueError("Value cannot be empty")
                elif not exit_str_avaliable and value.lower() == "exit":
                    # Set a value to None to exit input loop
                    value = None

            except ValueError as e:
                # Print error message in red for invalid input
                print(Fore.RED + f"Invalid data: {e}, please try again.\n")
            else:
                # Break out of input loop if the input is valid
                break

        return value
