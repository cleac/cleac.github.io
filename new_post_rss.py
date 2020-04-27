HOSTNAME = 'http://cleac.me/'


def identifier(it):
    return it


def program(*a, **kw):
    with open('.head', 'r') as storage:
        [filename,
         linkformat,
         rfcformat,
         title] = filter(identifier, storage.read().split('\n'))
    url = f'{HOSTNAME}{filename}#{linkformat}'

    return [
        '<item>\n',
        f'  <title>{title}</title>\n',
        f'  <link>{url}</link>\n',
        f'  <guid>{url}</guid>\n',
        f'  <pubDate>{rfcformat}</pubDate>\n',
        '</item>\n',
    ]
