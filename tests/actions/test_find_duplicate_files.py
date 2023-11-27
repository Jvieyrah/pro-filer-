from pro_filer.actions.main_actions import find_duplicate_files  # NOQA
import pytest
#Os seus testes rejeitam implementações de find_duplicate_files que consideram todos os arquivos em all_files como diferentes;
#Os seus testes rejeitam implementações de find_duplicate_files que consideram todos os arquivos em all_files como iguais;
#Os seus testes rejeitam implementações de find_duplicate_files que não levanta ValueError caso algum arquivo em all_files não exista;
#Os seus testes aprovam a implementação de find_duplicate_files presente em pro_filer/actions/main_actions.py;
#Os seus testes utilizam a fixture tmp_path para criar arquivos temporários.

def test_find_duplicate_files_with_empty_all_files():
    # Create a context object with an empty all_files key
    context = {"all_files": []}
    # Call the find_duplicate_files function with the context
    duplicate_files = find_duplicate_files(context)
    # Assert that the output matches the expected message
    assert duplicate_files == []

def test_find_duplicate_files_with_different_files(tmp_path):
    # Create a file with no extension within the temporary directory
    array_path = []
    for i in range(5):
        path = tmp_path / f"file{i}.txt"
        path.touch()
        path.write_text("a" * i)
        path = str(path)
        array_path.append(path)
       
    # Create a context object with the all_files key and the file path
    context = {"all_files": array_path}

    duplicate_files = find_duplicate_files(context)
    assert duplicate_files == []

def test_find_duplicate_files_with_equal_files(tmp_path):
    # Create a file with no extension within the temporary directory
    array_path = []
    for i in range(5):
        path = tmp_path / f"file{i}.txt"
        path.touch()
        path.write_text("a" * 5)
        path = str(path)
        array_path.append(path)
       
    # Create a context object with the all_files key and the file path
    context = {"all_files": array_path}

    duplicate_files = find_duplicate_files(context)
    assert duplicate_files == [(array_path[0], array_path[1]), (array_path[0], array_path[2]), (array_path[0], array_path[3]), (array_path[0], array_path[4]), (array_path[1], array_path[2]), (array_path[1], array_path[3]), (array_path[1], array_path[4]), (array_path[2], array_path[3]), (array_path[2], array_path[4]), (array_path[3], array_path[4])]

def test_find_duplicate_files_with_nonexistent_file(tmp_path):
    # Create a file with no extension within the temporary directory
    array_path = []
    for i in range(5):
        path = tmp_path / f"file{i}.txt"
        path.touch()
        path.write_text("a" * 5)
        path = str(path)
        array_path.append(path)
    array_path.append("file6.txt")
       
    # Create a context object with the all_files key and the file path
    context = {"all_files": array_path}

    with pytest.raises(ValueError) as excinfo:
        find_duplicate_files(context)
    assert "All files must exist" in str(excinfo.value)

def test_find_duplicate_files_with_mixed_equal_and_different_files(tmp_path):
    # Create a file with no extension within the temporary directory
    array_path = []
    for i in range(2):
        path = tmp_path / f"file{i}.txt"
        path.touch()
        path.write_text("a" * 5)
        path = str(path)
        array_path.append(path)
    for i in range(3):
        path = tmp_path / f"file{i+2}.txt"
        path.touch()
        path.write_text("a" * i)
        path = str(path)
        array_path.append(path)
       
    # Create a context object with the all_files key and the file path
    context = {"all_files": array_path}

    duplicate_files = find_duplicate_files(context)
    assert duplicate_files == [(array_path[0], array_path[1])]