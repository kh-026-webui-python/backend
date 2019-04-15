import csv


class CSVParser(object):

    def __init__(self, binary_mode=False):
        self.modes = binary_mode

    @property
    def modes(self):
        return self.__read_mode, self.__write_mode

    @modes.setter
    def modes(self, binary_mode):
        self.__read_mode, self.__write_mode = ('rb', 'wb') if binary_mode else ('r', 'w')

    def read(self, path, *fields):
        result = []
        with open(path, self.__read_mode) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                result.append({k: row.get(k, None) for k in fields})
        return result

    def write(self, path, *fields, writing_dictionaries=None):
        with open(path, self.__write_mode) as csv_file:
            writer = csv.DictWriter(csv_file, fields)
            writer.writeheader()
            if writing_dictionaries is not None:
                writer.writerows(writing_dictionaries)

    @classmethod
    def read_from_memory(cls, csv_file, *fields):
        result = []
        reader = csv.DictReader(csv_file)
        fieldnames = fields if fields else reader.fieldnames
        for row in reader:
            result.append({k: row.get(k, None) for k in fieldnames})
        return result
