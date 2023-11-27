import pytest
from pro_filer.actions.main_actions import show_disk_usage  # NOQA
from unittest.mock import Mock, patch
from pro_filer.cli_helpers import _get_printable_file_path

"""
def show_disk_usage(context):
    
    total_size = sum(os.path.getsize(file) for file in context["all_files"])

    for file_path in sorted(
        context["all_files"], key=os.path.getsize, reverse=True
    ):
        file_size = os.path.getsize(file_path)
        print(
            f"'{_get_printable_file_path(file_path)}':".ljust(70),
            f"{file_size} ({int(file_size / total_size * 100)}%)",
        )

    print(f"Total size: {total_size}")
"""
# _get_printable_file_path. must be mocked because it is imported from cli_helpers.py
# Os seus testes rejeitam implementações de show_disk_usage que não calculam corretamente o espaço total ocupado pelos arquivos listados em all_files;

def test_show_disk_usage_with_empty_all_files(capsys):
    # Create a context object with an empty all_files key
    context = {"all_files": []}
    # Call the show_disk_usage function with the context
    show_disk_usage(context)
    
    # Capture the output
    captured = capsys.readouterr()
    
    # Assert that the output matches the expected message
    assert captured.out == f"Total size: 0\n"

def test_show_disk_usage_with_wrong_file_size(capsys, tmp_path):
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
    # mock the _get_printable_file_path function

    expected_lines = [
        f"'file0':".ljust(70),
        f"'file1':".ljust(70),
        f"'file2':".ljust(70),
        f"'file3':".ljust(70),
        f"'file4':".ljust(70),
        f"Total size: 100"
    ]

    with patch("pro_filer.actions.main_actions._get_printable_file_path") as mock_get_printable_file_path:
        # set the return value of the _get_printable_file_path function
        mock_get_printable_file_path.return_value = "file0"
        # Call the show_disk_usage function with the context
        show_disk_usage(context)
        
        # Capture the output
        captured = capsys.readouterr()
        # expect asserttation error because the file size is wrong Xfail
        with pytest.raises(AssertionError):
            # Assert that the output matches the expected message
            for captured_line, expected_line in zip(captured.out.splitlines(), expected_lines):
                assert captured_line == expected_line



def test_show_disk_usage_with_correct_file_size(capsys, tmp_path):
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
    # mock the _get_printable_file_path function

  

    with patch("pro_filer.actions.main_actions._get_printable_file_path") as mock_get_printable_file_path:
        # for each time the _get_printable_file_path function is called, return the next value in the array_path
        return_values = iter(array_path)
        mock_get_printable_file_path.side_effect = lambda x: next(return_values)

        expected_lines = [
            f"'{str(tmp_path)}/file0.txt':".ljust(70)+" 4 (40%)",
            f"'{str(tmp_path)}/file1.txt':".ljust(70)+" 3 (30%)",
            f"'{str(tmp_path)}/file2.txt':".ljust(70)+" 2 (20%)",
            f"'{str(tmp_path)}/file3.txt':".ljust(70)+" 1 (10%)",
            f"'{str(tmp_path)}/file4.txt':".ljust(70)+" 0 (0%)",
            f"Total size: 10"
        ]
            
            

  
        


        # Call the show_disk_usage function with the context
        show_disk_usage(context)
        
        # Capture the output
        captured = capsys.readouterr()
        # Assert that the output matches the expected message
        for captured_line, expected_line in zip(captured.out.splitlines(), expected_lines):
            assert captured_line == expected_line
   
    
  
  