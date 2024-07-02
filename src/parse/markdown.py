from parse.utils import composition
import re

def start_count(string: str, char: str) -> int:
    count = 0
    while string.startswith(char * count):
        count += 1
    return count - 1


def handle_headers(string: str) -> str:
    match start_count(string, '#'):
        case 0:
            return string.strip()
        case 1:
            body = string.removeprefix('#').strip()
            return r"\section{!}".replace('!', body)
        case 2:
            body = string.removeprefix('##').strip()
            return r"\subsection{!}".replace('!', body)
        case count:
            body = string.removeprefix('#' * count).strip()
            return "\n" + r"\textit{!}".replace('!', body)


def apply_style(marker: str, statement: str):
    def func(s: str) -> str:
        start = s.find(marker)
        while True:
            end = s.find(marker, start + 1)
            if end == -1: break
            s = s[:start] + statement.replace("!", s[start+len(marker):end]) + s[end+len(marker):]
            start = s.find(marker)
        return s
    return func


def handle_quotes(s: str) -> str:
    start = s.find('"')
    while start != -1:
        end = s.find('"', start + 1)
        if end == -1: break
        s = s[:start] + "``" + s[start + 1:end] + "''" + s[end + 1:]
        start = s.find('"', start + 1)
    return s


handle_line = composition(
    handle_headers,
    apply_style("**", r"\textbf{!}"),
    apply_style("__", r"\textbf{!}"),
    apply_style("*", r"\textit{!}"),
    apply_style("`", r"\texttt{!}"),
    handle_quotes
)

itemize_markers = ('*', '-')
itemize = re.compile("^(\*|-)\s+ *")
enum = re.compile("^[0-9]+\.\s+ *")

def parse(source: list[str]) -> str:
    result = ""
    context = ""
    for line in source:
        if line == "\n":
            result += "\n"
            continue
        current: str = handle_line(line).rstrip()
        if len(current) == 0:
            continue
        if context:
            if itemize.match(current):
                current = r"\item " + itemize.split(current)[2]
            elif enum.match(current):
                current = r"\item " + enum.split(current)[1]
            else:
                current = r"\end{!}".replace('!', context) + "\n\n" + current
                context = ""
        else:
            if itemize.match(current):
                current = r"\begin{itemize}" + "\n" + r"\item " + itemize.split(current)[2]
                context = "itemize"
            elif enum.match(current):
                current = r"\begin{enumerate}" + "\n" + r"\item " + enum.split(current)[1]
                context = "enumerate"
        current = current.replace("_", r"\_")
        result += current + "\n"

    if context:
        result += r"\end{!}".replace('!', context)

    return result




