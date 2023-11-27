from pro_filer.actions.main_actions import show_details  # NOQA
import json
import os
from datetime import date
from faker import Faker

#context = {"base_path": "path/unexistant_file.json"} 
# create a contewxt object with a base_path key and a value of a non-existent file as show above using tmp_path)

def test_show_details_with_non_existent_file(capsys, tmp_path):
    # Create a non-existent file within the temporary directory
    path = tmp_path / "non_existent_file.json"
    path = str(path)
    # Create a context object with the base_path key and the non-existent file path
    context = {"base_path": path}    
    # Call the show_details function with the context
    show_details(context)
    
    # Capture the output
    captured = capsys.readouterr()
    
    # Assert that the output matches the expected message
    assert captured.out == f"File 'non_existent_file.json' does not exist\n"

def test_show_details_with_no_extension(capsys, tmp_path):
    # Create a file with no extension within the temporary directory
    path = tmp_path / "file"
    path.touch()
    path = str(path)
    # Create a context object with the base_path key and the file path
    context = {"base_path": path}    
    # Call the show_details function with the context
    show_details(context)
    
    # Capture the output
    captured = capsys.readouterr()
    filename = path.split('/')[-1]
    file_extension = os.path.splitext(filename)[1]
    py_mod_date = date.fromtimestamp(os.path.getmtime(path))
    
    expected_lines = [
     f"File name: {filename}",
     f"File size in bytes: {os.path.getsize(path)}",
     f"File type: {'directory' if os.path.isdir(path) else 'file'}",
     f"File extension: {file_extension or '[no extension]'}" ,
     f"Last modified date: {py_mod_date}"
    ]

    # Assert that the output matches the expected message
    for captured_line, expected_line in zip(captured.out.splitlines(), expected_lines):
        assert captured_line == expected_line
    


def test_show_details_with_json_file_and_file_bigger_than_0_kb(capsys, tmp_path):
    # Create a json file within the temporary directory
    path = tmp_path / "file.json"
    path.touch()
    # Write a json object to the file using the json.dump method fling it with faker data.
    faker_json = Faker()
    json_data = faker_json.json()
    with open(path, 'w') as f:
        json.dump(json_data, f)
    path = str(path)
    # Create a context object with the base_path key and the file path
    context = {"base_path": path}    
    # Call the show_details function with the context
    show_details(context)
    
    # Capture the output
    captured = capsys.readouterr()
    filename = path.split('/')[-1]
    file_extension = os.path.splitext(filename)[1]
    py_mod_date = date.fromtimestamp(os.path.getmtime(path))
    
    expected_lines = [
     f"File name: {filename}",
     f"File size in bytes: {os.path.getsize(path)}",
     f"File type: {'directory' if os.path.isdir(path) else 'file'}",
     f"File extension: {file_extension or '[no extension]'}" ,
     f"Last modified date: {py_mod_date}"
    ]

    # Assert that the output matches the expected message
    for captured_line, expected_line in zip(captured.out.splitlines(), expected_lines):
        assert captured_line == expected_line
