import os
from datetime import datetime
import errno
import sys
import shutil


ERROR_INVALID_NAME = 123


def change_dir(path: str = "", autocreate: bool = True) -> None:
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.
        autocreate (bool): Create folder if it doesn't exist.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
        ValueError: if path is invalid.
    Returns:
        Path of current directory
    """

    if not path:
        return os.getcwd()
    if not _check_path(path):
        raise ValueError(f'Path "{path}" is invalid')
    if not os.path.exists(path):
        if autocreate:
            os.mkdir(path)
        else:
            raise RuntimeError(f'Directory "{path}" does not exist and autocreate is False')
    os.chdir(path)
    return os.getcwd()


def get_files() -> list:
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """

    file_list = []
    filepath_list = os.listdir(os.getcwd())
    for file in filepath_list:
        try:
            file_list.append([
                              file,
                              datetime.fromtimestamp(os.stat(file).st_ctime),
                              datetime.fromtimestamp(os.stat(file).st_mtime),
                              os.stat(file).st_size
                             ])
        except FileNotFoundError as err:
            file_list.append([file, None, None, None])
    return file_list



def get_file_data(filename: str) -> dict:
    """Get full info about file.

    Args:
        filename (str): Filename.

    Returns:
        Dict, which contains full info about file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - edit_date (datetime): date of last file modification
        - size (int): size of file in bytes

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """
    path = os.path.join(os.getcwd(), filename)


    if not os.path.exists(path):
        raise RuntimeError(f'Filename "{filename}" does not exist')

    with open(path, 'rb') as file:
        return {
                'name': filename,
                'content': file.read(),
                'create_date': datetime.fromtimestamp(os.stat(path).st_ctime),
                'edit_date': datetime.fromtimestamp(os.stat(path).st_mtime),
                'size': os.stat(path).st_size
                }


def create_file(filename: str, content: str = '', overwrite: bool = False) -> dict:
    """Create a new file.

    Args:
        filename (str): Filename.
        content (str): String with file content.
        overwrite (bool): Create file if it already exist

    Returns:
        Dict, which contains name of created file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - size (int): size of file in bytes

    Raises:
        ValueError: if filename is invalid.
        RuntimeError: if file already exist and overwrite is False.
        OSError: if incorrect file creation
    """

    path = os.path.join(os.getcwd(), filename)

    if not _check_path(path):
        raise ValueError(f'Filename "{filename}" is invalid')

    if os.path.exists(path) and not overwrite:
        raise RuntimeError(f'File "{path}" already exist and overwrite is False')

    with open(path, 'wb') as file:
        if content:
            data = bytes(content, encoding='utf-8')
            file.write(data)

    with open(path, 'r') as file:
        if file.read() != content:
            raise OSError(f'Incorrect creation of file "{path}"')

        return {
                'name': filename,
                'content': bytes(content, encoding='utf-8'),
                'create_date': datetime.fromtimestamp(os.stat(path).st_ctime),
                'edit_date': datetime.fromtimestamp(os.stat(path).st_mtime),
                'size': os.stat(path).st_size
                }


def delete_file(filename: str) -> None:
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    path = os.path.join(os.getcwd(), filename)

    if not _check_path(path):
        raise ValueError(f'Filename "{filename}" is invalid')

    if not os.path.exists(path):
        raise RuntimeError('File {} does not exist'.format(filename))

    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def _check_path(path: str) -> bool:
    """
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    """
    try:
        if not isinstance(path, str) or not path:
            return False

        _, pathname = os.path.splitdrive(path)

        root_dirname = os.environ.get('HOMEDRIVE', 'C:') if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)

        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            except OSError as err:
                if hasattr(err, 'winerror'):
                    if err.winerror == ERROR_INVALID_NAME:
                        return False
                elif err.errno in {errno.ENAMETOOLONG}:
                    return False
    except TypeError:
        return False
    else:
        return True
