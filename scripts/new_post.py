import os
import os.path

from datetime import date, datetime
from email.utils import formatdate
from tempfile import NamedTemporaryFile

DATE_FORMAT = '%d-%b-%Y'
DATE_TEXT_FORMAT = '%d %B, %Y'
EDITOR = os.environ.get('EDITOR', 'vi')


def program(*a, **kw):
    filename = kw['filename']
    title = input('Enter title: ').strip()

    valid_file = False
    text_to_insert = ''
    while not valid_file:
        text_source = input('Do you want to put predefined contents? '
                            'Enter path to insert '
                            '(or just press Enter to open editor): ')
        if text_source:
            try:
                with open(text_source, 'r') as src:
                    text_to_insert = '\n  ' + src.read()
                os.remove(text_source)
            except FileNotFoundError:
                print(f'Could not open file: {text_source}\nPlease try again')
            except EOFError:
                return
            else:
                valid_file = True
        else:
            valid_file = True

    linkformat = date.today().strftime(DATE_FORMAT).lower()
    richformat = date.today().strftime(DATE_TEXT_FORMAT)
    rfcformat = formatdate(float(datetime.now().strftime('%s')))

    with NamedTemporaryFile() as tempfile:
        tempfile.write((f'<log-entry id="{linkformat}">\n'
                        f'  <h2>{richformat} - <a href="#{linkformat}">'
                        f'{title}</a></h2>{text_to_insert}'
                        '\n</log-entry>\n').encode('utf-8'))
        tempfile.flush()
        os.spawnvpe(os.P_WAIT, EDITOR, [EDITOR, tempfile.name], os.environ)
        tempfile.seek(0)
        result = [x.decode('utf-8') for x in tempfile.readlines()]

    with open('.head', 'w') as storage:
        storage.write(kw['filename'] + '\t\n')
        storage.write(linkformat + '\t\n')
        storage.write(rfcformat + '\t\n')
        storage.write(title + '\t\n')
        storage.write('\n'.join(result))

    feedname = os.path.splitext(filename)[0]
    os.spawnvpe(os.P_WAIT, 'rw.py', ('rw.py', feedname + '.rss'), os.environ)
    os.remove('.head')

    return result
