import os
import re

ban_to_sus = {
    "CE": "XG", "ce": "xg", "Cheat": "Xgods", "Engine": "Binary",
    "cheat": "xgods", "engine": "binary", "7.5": "0.0", "Trainer": "Brainer",
    "trainer": "brainer", "DBVM": "XGVM", "dbvm": "xgvm", "Dark Byte": "Duke Leto"
}

eng_to_greek = {
    "a": "α", "b": "β", "c": "ς", "d": "d", "e": "ε", "f": "ƒ", "g": "g", "h": "н", "i": "ι", "j": "j",
    "k": "κ", "l": "ℓ", "m": "м", "n": "η", "o": "ο", "p": "ρ", "q": "φ", "r": "я", "s": "s", "t": "τ",
    "u": "μ", "v": "v", "w": "ω", "x": "χ", "y": "λ", "z": "ζ"
}

def get_all_files_path_with_extension(ce_path, extension):
    return [os.path.join(foldername, filename)
            for foldername, _, filenames in os.walk(ce_path)
            for filename in filenames if filename.endswith(extension)]

def is_lfm_edit_line(text, keyword):
    return re.match(fr"\s+{keyword} = '[^']*'\s+", text, re.IGNORECASE)

def is_caption_line(text):
    return is_lfm_edit_line(text, "Caption")

def is_hint_line(text):
    return is_lfm_edit_line(text, "Hint")

def is_start_with_msgid(text):
    return text.strip().startswith("msgid")

def is_start_with_msgstr(text):
    return text.strip().startswith("msgstr")

def get_string_from_msgid(text):
    return [f"\"{string}\"" for string in re.findall(r"\"(.*?)\"", text)]

def get_strings_from_lfm_line(text):
    return [f"'{string}'" for string in re.findall(r"'(.*?)'", text)]

def ban_to_sus_string(text):
    for ban_text, sus_text in ban_to_sus.items():
        text = text.replace(ban_text, sus_text)
    return text

def build_greek_from_eng(eng_text):
    return ''.join(eng_to_greek.get(char.lower(), char) for char in eng_text)

def edit_string_in_file(file_path, is_lfm=False):
    edited_file_path = file_path + ".tmp"
    try:
        with open(file_path, 'r', encoding="utf-8") as original_file, open(edited_file_path, 'w', encoding="utf-8") as edited_file:
            msgid_inline_strings = []
            for line in original_file:
                line_for_write = line
                if is_lfm:
                    if is_caption_line(line_for_write) or is_hint_line(line_for_write):
                        inline_strings = get_strings_from_lfm_line(line_for_write)
                        for string in inline_strings:
                            string_no_ban = ban_to_sus_string(string)
                            line_for_write = line_for_write.replace(string, build_greek_from_eng(string_no_ban))
                else:
                    if is_start_with_msgid(line_for_write):
                        msgid_inline_strings = get_string_from_msgid(line_for_write)
                    if is_start_with_msgstr(line_for_write):
                        for string in msgid_inline_strings:
                            string_no_ban = ban_to_sus_string(string)
                            line_for_write = line_for_write.replace("\"\"", build_greek_from_eng(string_no_ban))
                edited_file.write(line_for_write)
        os.remove(file_path)
        os.rename(edited_file_path, file_path)
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    CE_PATH = 'C:\\Users\\User\\Documents\\GitHub\\Saucebitten\\Cheat Engine'
    EXTENSIONS = [".lfm", ".po", ".pot"]

    for extension in EXTENSIONS:
        file_paths = get_all_files_path_with_extension(CE_PATH, extension)
        for file_path in file_paths:
            if extension == ".lfm":
                edit_string_in_file(file_path, is_lfm=True)
            else:
                edit_string_in_file(file_path)
            print(f"edited {file_path}")
