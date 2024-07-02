from unittest import TestCase
from src.parse import markdown_package as markdown

class CountFunc(TestCase):

    def test_empty(self):
        actual = markdown.start_count("", '#')
        self.assertEqual(actual, 0)

    def test_0(self):
        actual = markdown.start_count("Abcs", '#')
        self.assertEqual(actual, 0)

    def test_1a(self):
        actual = markdown.start_count("# abcs", '#')
        self.assertEqual(actual, 1)

    def test_1b(self):
        actual = markdown.start_count("#abcs", '#')
        self.assertEqual(actual, 1)

    def test_2(self):
        actual = markdown.start_count("## abcs", '#')
        self.assertEqual(actual, 2)


class HeadersHandler(TestCase):

    def test_lvl0(self):
        actual = markdown.handle_headers(" words words ")
        self.assertEqual(actual, "words words")

    def test_lvl1(self):
        actual = markdown.handle_headers("# words words")
        self.assertEqual(actual, r"\section{words words}")

    def test_lvl2(self):
        actual = markdown.handle_headers("## words words")
        self.assertEqual(actual, r"\subsection{words words}")

    def test_lvl3(self):
        actual = markdown.handle_headers("### words words")
        self.assertEqual(actual, r"\textit{words words}")

    def test_lvl4(self):
        actual = markdown.handle_headers("#### words words")
        self.assertEqual(actual, r"\textit{words words}")


class StyleHandler(TestCase):
    def test_one_char_1(self):
        apply_style = markdown.apply_style('*', r'\textbf{!}')
        actual = apply_style("Text with *bold* word")
        self.assertEqual(actual, r"Text with \textbf{bold} word")

    def test_two_char_1(self):
        apply_style = markdown.apply_style('**', r'\textbf{!}')
        actual = apply_style("Text with **bold** word")
        self.assertEqual(actual, r"Text with \textbf{bold} word")


    def test_one_char_2(self):
        apply_style = markdown.apply_style('*', r'\textbf{!}')
        actual = apply_style("Text with *bold* word and *more one*")
        self.assertEqual(actual, r"Text with \textbf{bold} word and \textbf{more one}")


    def test_two_char_2(self):
        apply_style = markdown.apply_style('**', r'\textbf{!}')
        actual = apply_style("Text with **bold** word and **more one**")
        self.assertEqual(actual, r"Text with \textbf{bold} word and \textbf{more one}")


class QuotesHandle(TestCase):

    def test_1(self):
        actual = markdown.handle_quotes('Text "hello"')
        self.assertEqual(actual, "Text ``hello''")

    def test_2(self):
        actual = markdown.handle_quotes('Text "hello" and "world"')
        self.assertEqual(actual, "Text ``hello'' and ``world''")



class MarkdownTest(TestCase):

    def test_code_and_underscore1(self):
        text = "`y_train` - Numpy массив, содержащий разметку данных для x_train"
        actual = markdown.parse([text])
        expected = r"\texttt{y\_train} - Numpy массив, содержащий разметку данных для x\_train"
        self.assertEqual(actual.strip(), expected.strip())

    def test_itemize_and_quotes(self):
        text = r'* Renovation: уровень ремонта квартиры, например, "без ремонта", "косметический ремонт", "евроремонт" и т. д;'
        actual = markdown.parse([text])
        expected = (r"\begin{itemize}" "\n"
                    r"\item Renovation: уровень ремонта квартиры, например, ``без ремонта'', ``косметический ремонт'', ``евроремонт'' и т. д;" "\n"
                    r"\end{itemize}")
        self.assertEqual(actual.strip(), expected.strip())

    def test_2_itemize(self):
        data = [
            "* Number of floors: общее количество этажей в здании, где расположена квартира.\n",
            "* Renovation: уровень ремонта квартиры, например, \"без ремонта\", \"косметический ремонт\", \"евроремонт\" и т. д;"
        ]
        actual = markdown.parse(data)
        expected = (r'\begin{itemize}' '\n'
                    r'\item Number of floors: общее количество этажей в здании, где расположена квартира.' '\n'
                    r"\item Renovation: уровень ремонта квартиры, например, ``без ремонта'', ``косметический ремонт'', ``евроремонт'' и т. д;" "\n"
                    r'\end{itemize}'
                    r'')
        self.assertEqual(actual.strip(), expected.strip())


    def test_text_enum_enum_text(self):
        data = [
            "some text:\n",
            "1. one;\n",
            "2. two and finish.\n",
            "other text",
        ]
        actual = markdown.parse(data)
        expected = (r"some text:" "\n"
                    r"\begin{enumerate}" "\n"
                    r"\item one;" "\n"
                    r"\item two and finish." "\n"
                    r"\end{enumerate}" "\n\n"
                    r"other text")
        self.assertEqual(actual.strip(), expected.strip())