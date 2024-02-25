ERROR_PREFIX = "❗️"


def validate_number_of_people(text: str) -> None:
    if not text.isdigit():
        raise ValueError(ERROR_PREFIX + "Ожидалось целое число")
