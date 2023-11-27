"""Arquivo que estudantes devem editar"""

# criar uma função que retorna o arquivo mais profundo contido em context["all_files"] usando a quantidade de "/" como critério
def find_deepest_file(context):
    if not context["all_files"]:
        return None

    deepest_file = context["all_files"][0]

    for path in context["all_files"]:
        if path.count("/") > deepest_file.count("/"):
            deepest_file = path

    return deepest_file

def show_deepest_file(context):
    if not context["all_files"]:
        print("No files found")
    else:
        deepest_file = find_deepest_file(context)
        print(f"Deepest file: {deepest_file}")


def find_file_by_name(context, search_term, case_sensitive=True):
    if not search_term:
        return []

    found_files = []

    for path in context["all_files"]:
        file_name = path.split("/")[-1] # pega o último elemento da lista

        if not case_sensitive:
            file_name=file_name.lower()
            search_term=search_term.lower()

        if search_term in file_name:
            found_files.append(path)

    return found_files
