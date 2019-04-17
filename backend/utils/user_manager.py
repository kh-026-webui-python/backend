from hashlib import blake2b

from .transliteration import Transliterator


class UserManager(object):
    USER = ('username', 'email', 'first_name', 'last_name', 'password', 'profile')
    PROFILE = ('location', 'birth_date')
    SEPARATOR = "_"

    @classmethod
    def to_user_data(cls, input_dictionary):
        user_data = {key.lower().strip().replace(" ", cls.SEPARATOR): value for key, value in input_dictionary.items()}
        user_data[cls.USER[-1]] = {}
        for item in cls.PROFILE:
            if item in user_data:
                user_data[cls.USER[-1]][item] = user_data.pop(item)

        if cls.USER[0] not in user_data:
            user_data[cls.USER[0]] = cls.create_username(user_data)
        if cls.USER[-2] not in user_data:
            user_data[cls.USER[-2]] = cls.create_password(user_data)

        return user_data

    @classmethod
    def is_schema_correct(cls, user_data):
        for user_field in cls.USER:
            if user_field not in user_data:
                return False
        for profile_field in cls.PROFILE:
            if profile_field not in user_data[cls.USER[-1]]:
                return False
        return True

    @classmethod
    def create_password(cls, user_data):
        return blake2b(str(user_data).encode(), digest_size=8).hexdigest()

    @classmethod
    def create_username(cls, user_data):

        key_words = (
            user_data.get(cls.USER[-1]).get(cls.PROFILE[0], '  ')[:2],
            user_data.get(cls.USER[2], ''),
            user_data.get(cls.USER[3], ''),
            user_data.get(cls.USER[-1]).get(cls.PROFILE[1], '  ')[-2:],
        )

        return cls.SEPARATOR.join([Transliterator.transliterate(word.lower().strip()) for word in key_words])
