import datetime as dt


class User:
    """
    This class describes the user object of the mindreader package.
    Any changes to this class should be considered carefully.

    :attribute userame:

    """

    def __init__(self, user_id: int, username: str, birthday: int, gender: str):
        self.user_id = user_id
        self.username = username
        self.birthday = birthday
        self.gender = gender

    def __repr__(self):
        user_id = self.user_id
        username = self.username
        birthday = dt.datetime.fromtimestamp(self.birthday).strftime("%d/%m/%y")
        gender = self.gender
        return f'User(user_id={user_id}, username={username}, birthday={birthday}, gender={gender})'

    def __str__(self):
        user = f'user {self.user_id}'
        birthday = dt.datetime.fromtimestamp(self.birthday).strftime("%d/%m/%y")
        gender = 'male' if self.gender == 'm' else ('female' if self.gender == 'f' else None)
        str_rep = f'{user}: {self.username}, born {birthday}'
        if gender:
            str_rep += f' ({gender})'
        return str_rep
