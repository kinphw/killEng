class ANSIColor:
    COLORS = {
        "reset": "\033[0m",
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bold": "\033[1m",
        "underline": "\033[4m",
    }

    @staticmethod
    def colorize(text, color):
        """
        Wrap the given text with ANSI color codes.

        :param text: The text to colorize.
        :param color: The color name (e.g., 'red', 'green', 'blue').
        :return: Colorized text.
        """
        if color in ANSIColor.COLORS:
            return f"{ANSIColor.COLORS[color]}{text}{ANSIColor.COLORS['reset']}"
        return text

    @staticmethod
    def print_colored(text, color):
        """
        Print the given text with the specified color.

        :param text: The text to print.
        :param color: The color name (e.g., 'red', 'green', 'blue').
        """
        print(ANSIColor.colorize(text, color))

# Example usage
if __name__ == "__main__":
    ANSIColor.print_colored("This is a red text", "red")
    ANSIColor.print_colored("This is a green text", "green")
    ANSIColor.print_colored("This is a bold text", "bold")
