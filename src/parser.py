"""Parser for APT repository data."""


def read_local_repo(filepath):
    """Читает локальный файл репозитория и возвращает его текст."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise ValueError(f"Файл репозитория не найден: {filepath}")


def find_package_data(repo_content, package_name, package_version):
    """Ищет пакет в тексте репозитория."""
    blocks = repo_content.split("\n\n")
    for block in blocks:
        if not block.strip():
            continue
        lines = block.strip().split("\n")
        pkg_name_found = False
        version_found = False
        
        for line in lines:
            if line.startswith("Package: ") and line[9:] == package_name:
                pkg_name_found = True
            if line.startswith("Version: ") and line[9:] == package_version:
                version_found = True
                
        if pkg_name_found and version_found:
            return block
    return None


def extract_dependencies(package_block):
    """Извлекает список прямых зависимостей из блока пакета."""
    if not package_block:
        return []
    lines = package_block.split("\n")
    for line in lines:
        if line.startswith("Depends: "):
            deps_str = line[9:]
            return [d.split()[0] for d in deps_str.split(",") if d.strip()]
    return []