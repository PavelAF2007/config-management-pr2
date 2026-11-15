"""CLI application for dependency graph visualization."""
import argparse
import sys

# Константы (чтобы не было "магических чисел", как требует задание)
DEFAULT_MAX_DEPTH = 3
MAX_ALLOWED_DEPTH = 100


def parse_args(args):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Tool for visualizing package dependency graphs."
    )
    
    parser.add_argument(
        "--package", type=str, required=True,
        help="Name of the target package"
    )
    parser.add_argument(
        "--repo", type=str, required=True,
        help="URL of the repository or path to test repo"
    )
    parser.add_argument(
        "--test-mode", action="store_true",
        help="Enable test mode"
    )
    parser.add_argument(
        "--version", type=str, default="latest",
        help="Version of the package"
    )
    parser.add_argument(
        "--output", type=str, default="graph.svg",
        help="Name of the output image file"
    )
    parser.add_argument(
        "--ascii-tree", action="store_true",
        help="Output dependencies as ASCII tree"
    )
    parser.add_argument(
        "--max-depth", type=int, default=DEFAULT_MAX_DEPTH,
        help="Maximum depth of dependency analysis"
    )
    parser.add_argument(
        "--filter", type=str, default="",
        help="Substring to filter out packages"
    )
    
    return parser.parse_args(args)


def validate_args(args):
    """Проверяет аргументы на корректность."""
    # 1. Проверка глубины
    if args.max_depth <= 0:
        raise ValueError("Глубина (--max-depth) должна быть больше 0.")
        
    if args.max_depth > MAX_ALLOWED_DEPTH:
        raise ValueError(
            f"Слишком большая глубина. Максимум: {MAX_ALLOWED_DEPTH}."
        )
        
    # 2. Проверка расширения файла
    if not args.output.endswith(".svg"):
        raise ValueError("Имя файла (--output) должно заканчиваться на .svg")


def main():
    """Main entry point."""
    try:
        args = parse_args(None)
        
        # Вызываем функцию проверки
        validate_args(args) 
        
        # Вывод параметров
        print("--- Configuration ---")
        print(f"package: {args.package}")
        print(f"repo: {args.repo}")
        print(f"test_mode: {args.test_mode}")
        print(f"version: {args.version}")
        print(f"output: {args.output}")
        print(f"ascii_tree: {args.ascii_tree}")
        print(f"max_depth: {args.max_depth}")
        print(f"filter: {args.filter}")
        print("---------------------")
        
    except ValueError as error:
        # Если произошла ошибка, выводим её в консоль
        print(f"Ошибка: {error}", file=sys.stderr)
        # Завершаем программу с кодом ошибки (1)
        sys.exit(1) 


if __name__ == "__main__":
    main()