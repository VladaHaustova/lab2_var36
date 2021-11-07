import sys
import re
import json
import argparse

from typing import List
from tqdm import tqdm


class Entry:
    '''
    Объект класса Entry представляет запись с информацией о пользователе.
    Attributes
    ----------
      telephone : str
        телефон пользователя
      height : str
        рост пользователя
      snils : str
        снилс пользователя
      passport_series : str
        серия паспорта пользователя
      university : str
        университет пользователя
      work_experience : str
        рабочий стаж пользователя
      academic_degree : str
        степень пользователя
      worldview : str
        мировоззрение пользователя
      address : str
        адрес пользователя
    '''
    telephone: str
    height: str
    snils: str
    passport_series: str
    university: str
    work_experience: str
    academic_degree: str
    worldview: str
    address: str

    def __init__(self, dic: dict):
        self.curdict = dic
        self.telephone = dic['telephone']
        self.height = dic['height']
        self.snils = dic['snils']
        self.passport_series = dic['passport_series']
        self.university = dic['university']
        self.work_experience = dic['work_experience']
        self.academic_degree = dic['academic_degree']
        self.worldview = dic['worldview']
        self.address = dic['address']


class Validator:
    '''
    Объект класса Validator представляет валидатор записей.
    Он нужен для проверки введённых пользователем записей о
    телефоне, росте, стаже работы, снилсе, серии паспорта, степени, адреса
    на корректность.
    Attributes
    ----------
      entries : List[Entry]
        Список записей
    '''

    entries: List[Entry]

    def __init__(self, entries: List[Entry]):
        self.entries = []
        for i in entries:
            self.entries.append(Entry(i))

        #  self.entries = entries

    def parse(self) -> (List[List[str]], List[Entry]):
        '''
        Выполняет проверку корректности записей
        Returns
        -------
          (List[List[str]], List[Entry]):
            Пара: cписок списков неверных записей по названиям ключей
                                                и список верных записей
        '''

        illegal_entries = []
        legal_entries = []

        for i in self.entries:
            illkeys = self.parse_entry(i)

            if len(illkeys) != 0:
                illegal_entries.append(illkeys)
            else:
                legal_entries.append(i)
        return (illegal_entries, legal_entries)

    def parse_entry(self, entry: Entry) -> List[str]:
        '''
        Выполняет проверку корректности одной записи
        Returns
        -------
          List[str]:
            Список неверных ключей в записи
        '''

        illegal_keys = []

        if not self.check_telephone(entry.telephone):
            illegal_keys.append('telephone')
        elif not self.check_snils(entry.snils):
            illegal_keys.append('snils')
        elif not self.check_passport(entry.passport_series):
            illegal_keys.append('passport_series')
        elif not self.check_height(entry.height):
            illegal_keys.append('height')
        elif not self.check_work_experience(entry.work_experience):
            illegal_keys.append('work_experience')
        elif not self.check_address(entry.address):
            illegal_keys.append('address')
        elif not self.check_university(entry.university):
            illegal_keys.append('university')
        elif not self.check_degree(entry.academic_degree):
            illegal_keys.append('academic_degree')
        elif not self.check_worldview(entry.worldview):
            illegal_keys.append('worldview')

        return illegal_keys

    def check_telephone(self, telephone: str) -> bool:
        '''
        Выполняет проверку корректности номера телефона.
        Если в строке присутствуют пробелы, запятые, двойные точки, буквы,
        то будет возвращено False.
        Parameters
        ----------
          telephone : str
            Строка с проверяемым номером телефона
        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''
        pattern = '^(\+7[\-][(]\d{3}[)][\-]\d{3}[\-]\d{2}[\-]\d{2})$'
        if re.match(pattern, telephone):
            return True
        return False

    def check_snils(self, snils: str) -> bool:
        '''
        Выполняет проверку корректности снилса.
        Если строка состоит не из 11-ти цифр, возвращает False
        Parameters
        ----------
          snils : str
            Строка с проверяемым снилсом
        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        pattern = '^\\d{11}$'

        if re.match(pattern, snils):
            return True
        return False

    def check_passport(self, passport: str) -> bool:
        '''
        Выполняет проверку корректности серии паспорта.
        Если строка состоит не из четырёх цифр разделённых попарно пробелом, возвращает False
        Parameters
        ----------
          passport : str
            Строка с проверяемой серией
        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        pattern = '^\\d{2} \\d{2}$'

        if re.match(pattern, passport):
            return True
        return False

    def check_height(self, height: str) -> bool:
        '''
        Выполняет проверку корректности роста пользователя.
        Возврашщает True, если рост находится в пределах 1.20..2.10
        Parameters
        ----------
          height : str
            Строка с проверяемым ростом
        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        try:
            fheight = float(height)
        except ValueError:
            return False

        return fheight > 1.20 and fheight < 2.10

    def check_work_experience(self, work_experience: str) -> bool:
        '''
        Выполняет проверку корректности опыта работы.
        Возврашщает True, если опыт работы в годах находится в пределах 2..20
        Parameters
        ----------
          work_experience : str
            Строка с проверяемым опытом
        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        try:
            iyears = int(work_experience)
        except ValueError:
            return False

        return iyears >= 2 and iyears < 20

    def check_address(self, address: str) -> bool:
        '''
        Выполняет проверку корректности адреса пользователя.
        Возврашщает True, строка состоит из букв русского алфавита и знака '-', а также
        строка разделена на улицу и номер дома, состоящего из цифр
        Parameters
        ----------
          address : str
            Строка с проверяемым адресом
        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        pattern = '^[а-яА-Я-\s]+\d+$'

        if re.match(pattern, address):
            return True
        return False

    def check_university(self, university: str) -> bool:
        '''
        Выполняет проверку корректности университета пользователя.
        Возвращает True, строка состоит из букв русского алфавита, знака '-' или '.' или пробела
        Parameters
        ----------
          university : str
            Строка с проверяемой профессией
        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        pattern = '^[а-яА-Я-\s\.]+$'

        if re.match(pattern, university):
            return True
        return False

    def check_degree(self, degree: str) -> bool:
        '''
        Выполняет проверку корректности степени пользователя.
        Возврашщает True, строка состоит из букв русского/английского алфавита, знака '-' или пробела
        Parameters
        ----------
          degree : str
            Строка с проверяемой степенью
        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        pattern = '^[a-zA-Zа-яА-Я -]+$'

        if re.match(pattern, degree):
            return True
        return False

    def check_worldview(self, worldview: str) -> bool:
        '''
        Выполняет проверку корректности мировоззрения пользователя.
        Возврашщает True, строка состоит из букв русского/английского алфавита, знака '-' или пробела
        Parameters
        ----------
          worldview : str
            Строка с проверяемым мировоззрением
        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        pattern = '^[a-zA-Zа-яА-Я -]+$'

        if re.match(pattern, worldview):
            return True
        return False


def show_summary(result: List[List[str]], filename: str = ''):
    '''
      Выдаёт итоговую информацию об ошибках в записях
      Parameters
      ----------
        result : List[List[str]]
          Список списков неверных записей по названиям ключей
    '''

    all_errors_count = 0
    errors_count = {
        'telephone': 0,
        'height': 0,
        'snils': 0,
        'passport_series': 0,
        'university': 0,
        'work_experience': 0,
        'academic_degree': 0,
        'worldview': 0,
        'address': 0,
    }

    for i in result:
        for j in i:
            errors_count[j] += 1
            all_errors_count += 1

    if filename == '':
        print('\nВсего ошибок: %d\n' % all_errors_count)
        print('Количество ошибок по типам: ')

        for key, value in errors_count.items():
            print(key, ': ', value, sep='')
    else:
        with open(filename, 'w') as file:
            file.write('Всего ошибок: %d\n' % all_errors_count)

            for key, value in errors_count.items():
                file.write(key + ': ' + str(value) + '\n')


def save_in_json(data: List[Entry], filename: str):
    '''
        Выдаёт итоговую информацию о верных записях в формате json
        Parameters
        ----------
          data : List[Entry]
            Список верных записей
          filename : str
            Имя файла для записи
    '''
    f = open(filename, 'w')

    f.write('[')

    for i in data:
        f.write('''
    {
      "telephone": "%s",
      "height": %s,
      "snils": "%s",
      "passport_series": "%s",
      "university": "%s",
      "work_experience": %s,
      "academic_degree": "%s",
      "worldview": "%s",
      "address": "%s",
    },''' % (i.telephone, i.height, i.snils, i.passport_series, i.university, i.work_experience, i.academic_degree,
             i.worldview, i.address))
    f.write('\n]')
    f.close()


if len(sys.argv) < 2:
    input_file = '36.txt'
    output_file = '36_result.txt'
else:
    parser = argparse.ArgumentParser(
        description='Make users\' entries validation.')
    parser.add_argument('-input_file', metavar='input_file', nargs=1, type=str,
                        help='input file name')
    parser.add_argument('-output_file', metavar='output_file', nargs=1, type=str,
                        help='output file name')

    args = parser.parse_args()

    input_file = args.input_file[0]
    output_file = args.output_file[0]

val = Validator([])

with tqdm(total=100) as progressbar:
    data = json.load(open(input_file, encoding='windows-1251'))
    progressbar.update(60)

    val = Validator(data)
    res = val.parse()

    progressbar.update(40)

    show_summary(res[0], output_file)
    save_in_json(res[1], 'valid_data.txt')
