
# Format number
def format_number(current_number, match_number):

    """
        Give current number an 
    """

    current_number_string = f"{current_number}"
    match_number_string = f"{match_number}"

    if "." in match_number_string:
        match_decimals = len(match_number_string.split('.')[1])
        current_number_string = f"{current_number:.{match_decimals}f}"
        current_number_string = current_number_string[:]
        return current_number_string
    else:
        return f'{int(current_number)}'