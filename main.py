from pathlib import Path
from shutil import move
from time import time

from file_format import categories 

download_path = Path.home() / "Downloads"

def reverse_dictionary(dictionary):
    reverse_dictionary = {}
    for key, values in dictionary.items():
        for value in values:
            reverse_dictionary[value] = key
    
    return reverse_dictionary

def get_unique_target_path(target_dir, filename):
    target = target_dir / filename

    if not target.exists():
        return target

    base = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1

    while True:
        new_name = (f"{base}_conflict{counter}{suffix}")
        new_target = target_dir / new_name

        if not new_target.exists():
            return new_target
        
        counter += 1

def make_dirs(paths):
    for path in paths:
        directory = download_path / path 

        if directory.exists() and directory.is_file():
            new_path = get_unique_target_path(directory.parent, directory.name)
            directory.rename(new_path)
            print(f"Файл {directory} переименован в {new_path}")
        directory.mkdir(parents=True, exist_ok=True)

def moves_file(data):
    category_folders = set(categories.keys()) | {"Другое"}
    
    for file in download_path.iterdir():
        if file.is_dir() and file.name in category_folders:
            continue

        category = data.get(file.suffix, "Другое")
        target_dir = download_path / category
        target_path = get_unique_target_path(target_dir, file.name)
        move(file, target_path)
        
start = time()

reverse_categories = reverse_dictionary(categories)
all_categories = set(categories.keys()) | {"Другое"}
make_dirs(all_categories)
moves_file(reverse_categories)

end = time()
print(f"Время выполнения: {end - start} сек.")