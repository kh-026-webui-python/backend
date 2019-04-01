class Transliterator(object):

    TRANS_TABLE = (

        (u"щ", u"sch"),

        (u"ё", u"yo"),
        (u"ж", u"zh"),
        (u"ц", u"ts"),
        (u"ч", u"ch"),
        (u"ш", u"sh"),
        (u"ы", u"yi"),
        (u"ю", u"yu"),
        (u"я", u"ya"),

        (u"а", u"a"),
        (u"б", u"b"),
        (u"в", u"v"),
        (u"г", u"g"),
        (u"д", u"d"),
        (u"е", u"e"),
        (u"з", u"z"),
        (u"и", u"i"),
        (u"й", u"j"),
        (u"к", u"k"),
        (u"л", u"l"),
        (u"м", u"m"),
        (u"н", u"n"),
        (u"о", u"o"),
        (u"п", u"p"),
        (u"р", u"r"),
        (u"с", u"s"),
        (u"т", u"t"),
        (u"у", u"u"),
        (u"ф", u"f"),
        (u"х", u"h"),
        (u"э", u"e"),
        (u"ъ", u""),
        (u"ь", u""),

        (u"c", u"c"),
        (u"q", u"q"),
        (u"y", u"y"),
        (u"x", u"x"),
        (u"w", u"w"),
        (u"1", u"1"),
        (u"2", u"2"),
        (u"3", u"3"),
        (u"4", u"4"),
        (u"5", u"5"),
        (u"6", u"6"),
        (u"7", u"7"),
        (u"8", u"8"),
        (u"9", u"9"),
        (u"0", u"0"),
    )  #: Translation table

    @classmethod
    def transliterate(cls, input_string, strict=True):

        """
        Transliterate russian text
        @param input_string: input string
        @type input_string: C{unicode}
        @param strict: raise error if transliteration is incomplete.
            (True by default)
        @type strict: C{bool}
        @return: transliterated string
        @rtype: C{str}
        @raise ValueError: when string doesn't transliterate completely.
            Raised only if strict=True
        """
        transliteration = input_string
        for input_char, output_char in cls.TRANS_TABLE:
            transliteration = transliteration.replace(input_char, output_char)

        if strict and any(ord(char) > 128 for char in transliteration):
            raise ValueError("Unicode string doesn't transliterate completely, " +
                             "is it russian?")

        return transliteration
