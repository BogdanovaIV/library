import uuid


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
                value = input(text_message)

                if value.lower() == "exit":
                    value = None
                else:
                    value = int(value)

            except ValueError as e:
                print(f"Invalid data: {e}, please try again.\n")
            else:
                break

        return value

    @staticmethod
    def input_str(text_message, empty_str_avaliable=False):
        """
        Input the value which is a string.

        Args:
            text_message (str): The message is sent to the user.

        Returns:
            string or None: The value inputted by the user.
        """
        value = None
        while True:
            try:
                value = input(text_message)

                if not empty_str_avaliable and not value:
                    raise ValueError("Value cannot be empty")
                elif value.lower() == "exit":
                    value = None

            except ValueError as e:
                print(f"Invalid data: {e}, please try again.\n")
            else:
                break

        return value
