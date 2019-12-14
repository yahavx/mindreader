from pathlib import Path
import os
from flask import Flask

website = Flask(__name__)
data_dir = None

response_404 = '''
<html>
    <head>
        <title>Error 404 (page not found)</title>
    </head>
    <body>
        Error 404: page not found.
    </body>
</html>
'''


@website.route('/users/<int:user_id>')
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

    curr_path = f'{str(data_dir)}/{user_id}'
    user_thought = []

    if not os.path.exists(curr_path):
        return

    for file_dir in Path(curr_path).iterdir():
        file_data = open(file_dir).read()
        file_name = file_dir.stem.split('_')  # change display name to correct format
        file_name[1] = file_name[1].replace('-', ':')
        file_name = ' '.join(file_name)
        user_thought.append(_THOUGHT_LINE_HTML.format(file_name=file_name, thought=file_data))
    user_html = _USER_HTML.format(user_id=user_id, user_thoughts='\n'.join(user_thought))
    return user_html


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
    for user_dir in Path(data_dir).iterdir():
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    index_html = _INDEX_HTML.format(users='\n'.join(users_html))
    return index_html


def run_webserver(address, data_dirr):
    global data_dir
    data_dir = data_dirr
    website.run(*address)
