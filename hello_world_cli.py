#!/usr/bin/env python3
"""A small CLI for printing Hello World snippets in popular languages."""

from __future__ import annotations

import argparse
import sys


HELLO_WORLDS: dict[str, str] = {
    "python": 'print("Hello, World!")',
    "javascript": 'console.log("Hello, World!");',
    "typescript": 'console.log("Hello, World!");',
    "java": "\n".join(
        [
            "public class Main {",
            "    public static void main(String[] args) {",
            '        System.out.println("Hello, World!");',
            "    }",
            "}",
        ]
    ),
    "c": "\n".join(
        [
            "#include <stdio.h>",
            "",
            "int main(void) {",
            '    printf("Hello, World!\\n");',
            "    return 0;",
            "}",
        ]
    ),
    "cpp": "\n".join(
        [
            "#include <iostream>",
            "",
            "int main() {",
            '    std::cout << "Hello, World!" << std::endl;',
            "    return 0;",
            "}",
        ]
    ),
    "csharp": "\n".join(
        [
            "using System;",
            "",
            "Console.WriteLine(\"Hello, World!\");",
        ]
    ),
    "go": "\n".join(
        [
            "package main",
            "",
            'import "fmt"',
            "",
            "func main() {",
            '    fmt.Println("Hello, World!")',
            "}",
        ]
    ),
    "rust": "\n".join(
        [
            "fn main() {",
            '    println!("Hello, World!");',
            "}",
        ]
    ),
    "ruby": 'puts "Hello, World!"',
    "php": "\n".join(
        [
            "<?php",
            'echo "Hello, World!\\n";',
        ]
    ),
    "swift": 'print("Hello, World!")',
    "kotlin": "\n".join(
        [
            "fun main() {",
            '    println("Hello, World!")',
            "}",
        ]
    ),
}

ALIASES: dict[str, str] = {
    "js": "javascript",
    "ts": "typescript",
    "c++": "cpp",
    "cs": "csharp",
    "c#": "csharp",
    "golang": "go",
    "kt": "kotlin",
    "rb": "ruby",
}


def normalize_language(language: str) -> str:
    key = language.strip().lower()
    return ALIASES.get(key, key)


def available_languages() -> list[str]:
    return sorted(HELLO_WORLDS)


def get_snippet(language: str) -> str | None:
    return HELLO_WORLDS.get(normalize_language(language))


def choose_interactively() -> str:
    languages = available_languages()
    print("Choose a language:")
    for index, language in enumerate(languages, start=1):
        print(f"{index:>2}. {language}")

    while True:
        choice = input("Language number or name: ").strip()
        if not choice:
            print("Please enter a language number or name.")
            continue

        if choice.isdigit():
            selected_index = int(choice)
            if 1 <= selected_index <= len(languages):
                return languages[selected_index - 1]

        normalized = normalize_language(choice)
        if normalized in HELLO_WORLDS:
            return normalized

        print(f"Unknown language: {choice}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Print a Hello World snippet for a selected programming language."
    )
    parser.add_argument(
        "language",
        nargs="?",
        help="Language to print, for example python, js, java, go, rust, cpp.",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List supported languages.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list:
        print("\n".join(available_languages()))
        return 0

    language = normalize_language(args.language) if args.language else choose_interactively()
    snippet = get_snippet(language)
    if snippet is None:
        print(f"Unknown language: {args.language}", file=sys.stderr)
        print("Run with --list to see supported languages.", file=sys.stderr)
        return 1

    print(snippet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
