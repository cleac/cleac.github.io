import os

from datetime import date
from tempfile import NamedTemporaryFile

DATE_FORMAT = '%d-%b-%Y'
DATE_TEXT_FORMAT = '%d %B, %Y'
EDITOR = os.environ.get('EDITOR', 'vi')


def program():
    title = input('Enter title: ')
    dateformat = date.today().strftime(DATE_FORMAT).lower()
    richformat = date.today().strftime(DATE_TEXT_FORMAT)
    with NamedTemporaryFile() as tempfile:
        tempfile.write((f'<log-entry id="{dateformat}">\n'
                        f'  <h2>{richformat} - <a href="#{dateformat}">'
                        f'{title}</a></h2>\n</log-entry>\n').encode('utf-8'))
        tempfile.flush()
        os.spawnvpe(os.P_WAIT, EDITOR, [EDITOR, tempfile.name], os.environ)
        tempfile.seek(0)
        return [x.decode('utf-8') for x in tempfile.readlines()]
