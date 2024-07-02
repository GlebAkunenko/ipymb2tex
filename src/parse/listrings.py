pattern = r"""
\begin{lstlisting}[language={[LANG]},caption={}]
[CODE]
\end{lstlisting}
"""


def parse_code(source: list[str]) -> str:
	return pattern.replace("[CODE]", "".join(source)).replace('[LANG]', 'Python')


def parse_result(source: list[str]) -> str:
	return pattern.replace("[CODE]", "".join(source)).replace('[LANG]', '')