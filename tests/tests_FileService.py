import os
import pytest

from server import FileService


@pytest.fixture(scope='function')
def file_creation(request):
    FileService.create_file("test_for_delete.txt", overwrite=True)


@pytest.fixture(scope='function')
def file_delete(request):
    if os.path.exists(os.path.join(os.getcwd(), "test_ok.txt")):
        FileService.delete_file(filename=os.path.join(os.getcwd(), "test_ok.txt"))


# change dir
def test_change_dir_autocreate_true(path="test"):
    start_dir = os.path.join(os.getcwd(), "test")
    FileService.change_dir(path=path, autocreate=True)
    assert os.getcwd() == start_dir


def test_change_dir_autocreate_false(path="not_creating_folder"):
    with pytest.raises(RuntimeError):
        FileService.change_dir(path=path, autocreate=False)


def test_change_dir_incorrect_name(path=os.path.join(os.getcwd(), "tes&?t")):
    with pytest.raises(ValueError):
        FileService.change_dir(path=path, autocreate=False)


# get files
def test_get_files():
    f = FileService.get_files()
    assert isinstance(f, list)


# write file data
def test_create_file_value_error(filename=os.path.join(os.getcwd(), "filename_incorrect&?.txt")):
    with pytest.raises(ValueError):
        FileService.create_file(filename=filename, content="test content")

@pytest.mark.usefixtures('file_delete')
def test_create_file_all_ok(filename=os.path.join(os.getcwd(), "test_ok.txt")):
    stat = FileService.create_file(filename=filename, content="test content", overwrite=True)
    assert isinstance(stat, dict)
    assert "name" in stat
    assert "content" in stat
    assert "create_date" in stat
    assert "edit_date" in stat
    assert "size" in stat

@pytest.mark.usefixtures('file_delete')
def test_create_file_overwrite_false(filename=os.path.join(os.getcwd(), "test_ok.txt")):
    with pytest.raises(RuntimeError):
        FileService.create_file(filename=filename, content="test content", overwrite=False)


# get file data
def test_get_file_data_runtime_error(filename=os.path.join(os.getcwd(), "test_no_file.txt")):
    with pytest.raises(RuntimeError):
        FileService.get_file_data(filename=filename)


def test_get_file_data_value_error(filename=os.path.join(os.getcwd(), "filename_incorrect&?.txt")):
    with pytest.raises(ValueError):
        FileService.get_file_data(filename=filename)


def test_get_file_data_all_ok(filename=os.path.join(os.getcwd(), "test_ok.txt")):
    stat = FileService.get_file_data(filename=filename)
    assert isinstance(stat, dict)
    assert "name" in stat
    assert "content" in stat
    assert "create_date" in stat
    assert "edit_date" in stat
    assert "size" in stat


# delete file
def test_delete_file_runtime_error(filename=os.path.join(os.getcwd(), "test_no_file.txt")):
    with pytest.raises(RuntimeError):
        FileService.get_file_data(filename=filename)


def test_delete_file_value_error(filename=os.path.join(os.getcwd(), "te?st.txt")):
    with pytest.raises(ValueError):
        FileService.delete_file(filename=filename)


@pytest.mark.usefixtures('file_creation')
def test_delete_file_all_ok(filename="test_for_delete.txt"):
    assert FileService.delete_file(filename=filename)
