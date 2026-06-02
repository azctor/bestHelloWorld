import contextlib
import io
import unittest

import hello_world_cli


class HelloWorldCliTest(unittest.TestCase):
    def test_list_includes_popular_languages(self):
        languages = hello_world_cli.available_languages()

        self.assertIn("python", languages)
        self.assertIn("javascript", languages)
        self.assertIn("perl", languages)
        self.assertIn("rust", languages)

    def test_get_snippet_accepts_aliases(self):
        self.assertEqual(
            hello_world_cli.get_snippet("js"), 'console.log("Hello, World!");'
        )
        self.assertTrue(hello_world_cli.get_snippet("c++").startswith("#include <iostream>"))
        self.assertTrue(hello_world_cli.get_snippet("c#").startswith("using System;"))
        self.assertEqual(
            hello_world_cli.get_snippet("pl"), 'print "Hello, World!\\n";'
        )

    def test_main_prints_requested_language(self):
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            exit_code = hello_world_cli.main(["go"])

        self.assertEqual(exit_code, 0)
        self.assertIn('fmt.Println("Hello, World!")', stdout.getvalue())

    def test_main_returns_error_for_unknown_language(self):
        stderr = io.StringIO()

        with contextlib.redirect_stderr(stderr):
            exit_code = hello_world_cli.main(["brainfuck"])

        self.assertEqual(exit_code, 1)
        self.assertIn("Unknown language: brainfuck", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
