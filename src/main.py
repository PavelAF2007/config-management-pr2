"""CLI application for dependency graph visualization."""
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from parser import read_local_repo
from graph import DependencyGraph

DEFAULT_MAX_DEPTH = 3
MAX_ALLOWED_DEPTH = 100


def parse_args(args):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Tool for visualizing package dependency graphs."
    )
    parser.add_argument("--package", type=str, required=True)
    parser.add_argument("--repo", type=str, required=True)
    parser.add_argument("--test-mode", action="store_true")
    parser.add_argument("--version", type=str, default="latest")
    parser.add_argument("--output", type=str, default="graph.svg")
    parser.add_argument("--ascii-tree", action="store_true")
    parser.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH)
    parser.add_argument("--filter", type=str, default="")
    return parser.parse_args(args)


def validate_args(args):
    """Валидация аргументов."""
    if args.max_depth <= 0:
        raise ValueError("Глубина должна быть больше 0.")
    if args.max_depth > MAX_ALLOWED_DEPTH:
        raise ValueError(f"Максимум глубины: {MAX_ALLOWED_DEPTH}.")
    if not args.output.endswith(".svg"):
        raise ValueError("Файл должен иметь расширение .svg")


def main():
    """Main entry point."""
    try:
        args = parse_args(None)
        validate_args(args)
        
        print("--- Configuration ---")
        print(f"package: {args.package}, max_depth: {args.max_depth}")
        print(f"test_mode: {args.test_mode}")
        
        if args.test_mode:
            print("\n--- Сбор данных (Этап 2) ---")
            repo_content = read_local_repo(args.repo)
            
            graph = DependencyGraph(repo_content)
            graph.build_graph(args.package, args.max_depth, args.filter)
            
            print(f"\n--- Граф зависимостей для {args.package} ---")
            for pkg, deps in graph.graph.items():
                print(f"{pkg} -> {', '.join(deps) if deps else 'нет'}")
                
            print(f"\n--- Обратные зависимости (Этап 4) ---")
            rev_deps = graph.get_reverse_dependencies(args.package)
            print(f"Пакеты, зависящие от {args.package}:")
            for rd in rev_deps:
                print(f" - {rd}")
        else:
            print("\n[Режим реального URL пока не реализован]")

    except ValueError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()