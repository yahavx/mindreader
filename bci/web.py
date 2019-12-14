from pathlib import Path
from .website import Website
import os

website = Website()
data_path = ''


@website.route('/users/([0-9]+)')
def user(user_id):
    _USER_HTML = '''
    <html>
        <link rel="icon" href="data:;base64,iVBORw0KGgo=">
        <head>
            <title>Brain Computer Interface: User {user_id}</title>
        </head>
        <body>
            <table>
                {user_thoughts}
            </table>
        </body>
    </html>
    '''

    _THOUGHT_LINE_HTML = '''
    <tr>
        <td>{file_name}</td>
        <td>{thought}</td>
    </tr> 
    '''

    curr_path = f'{str(data_path)}/{user_id}'
    user_thought = []

    if not os.path.exists(curr_path):
        return 404, ''

    for file_dir in Path(curr_path).iterdir():
        file_data = open(file_dir).read()
        file_name = file_dir.stem.split('_')  # 3 next lines to change file display name to correct format
        file_name[1] = file_name[1].replace('-', ':')
        file_name = ' '.join(file_name)
        user_thought.append(_THOUGHT_LINE_HTML.format(file_name=file_name, thought=file_data))
    user_html = _USER_HTML.format(user_id=user_id, user_thoughts='\n'.join(user_thought))
    return 200, user_html


@website.route('/')
def index():
    _INDEX_HTML = '''
    <html>
        <link rel="icon" href="data:;base64,iVBORw0KGgo=">
        <head>
            <title>Brain Computer Interface</title>
        </head>
        <body>
            <ul>
                {users}
            </ul>
        </body>
    </html>
    '''

    _USER_LINE_HTML = '''
    <li><a href="/users/{user_id}">user {user_id}</a></li>
    '''

    users_html = []
    for user_dir in Path(data_path).iterdir():
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    index_html = _INDEX_HTML.format(users='\n'.join(users_html))
    return 200, index_html


def run_webserver(address, data_dir):
    global data_path
    data_path = data_dir
    website.run(address)


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1

    ip, port = argv[1].split(':')
    port = int(port)
    data_path = argv[2]
    try:
        run_webserver((ip, port), data_path)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
