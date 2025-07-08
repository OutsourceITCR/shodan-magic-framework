import re


def replace_word_in_file(file_path, search, replace):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        new_content = re.sub(search, replace, content)

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(new_content)

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
