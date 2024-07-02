import base64

def save_image_from_string(data: str, file_name: str):
    with open(file_name, "wb") as fh:
        fh.write(base64.decodebytes(bytes(data, 'utf-8')))


_patter = r"""
\begin{figure}[h!]
  \centering
  \includegraphics[width=0.9\textwidth]{img/[INDEX].png}
  \caption{}
  \label{fig:[INDEX]}
\end{figure}
"""

image_number = 1

def parse(output_path: str, data: str) -> str:
    global image_number
    save_image_from_string(data, f"{output_path}/{image_number}.png")
    result = _patter.replace("[INDEX]", str(image_number))
    image_number += 1
    return result