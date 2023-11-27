from pro_filer.actions.main_actions import show_preview  # NOQA
from faker import Faker
from faker.providers import lorem



def test_show_preview_with_all_file_andall_dirs_empty(capsys):
    context = {"all_files": [], "all_dirs": []}
    show_preview(context)
    captured = capsys.readouterr()
    assert captured.out == "Found 0 files and 0 directories\n"

def test_show_preview_with_all_file_andall_dirs(capsys):
    context = {"all_files": ["/path/to/file.txt"], "all_dirs": ["/path/to"]}
    show_preview(context)
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()
    expected_lines = [
        "Found 1 files and 1 directories",
        "First 5 files: ['/path/to/file.txt']",
        "First 5 directories: ['/path/to']",
    ]

    for captured_line, expected_line in zip(captured_lines, expected_lines):
        assert captured_line == expected_line

faker = Faker()
ten_files = [f"/path/to/file{i}.txt" for i in range(10)]
ten_paths = list(set([faker.file_path() for _ in range(10)]))

context = {"all_files": ten_files, "all_dirs": ten_paths}

def test_show_preview_with_all_file_andall_dirs_when_more_than_5_files(capsys):
    show_preview(context)
    captured = capsys.readouterr()
    captured_lines = captured.out.splitlines()
    expected_lines = [
        "Found 10 files and 10 directories",
        f"First 5 files: {ten_files[:5]}", 
        f"First 5 directories: {ten_paths[:5]}",
    ]

    for captured_line, expected_line in zip(captured_lines, expected_lines):
        assert captured_line == expected_line
  

