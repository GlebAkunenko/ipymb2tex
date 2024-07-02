import json
import parse

def run(input_path: str, output_path: str):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)['cells']
        result = ""
        for block in data:
            match block:
                case {'cell_type': "markdown", 'source': source}:
                    result += parse.markdown(source)
                case {'cell_type': "code", 'source': source, 'outputs': outputs}:
                    result += parse.code(source)
                    if len(outputs):
                        for output in outputs:
                            match output:
                                case {'output_type': "execute_result", 'data': {'text/html': table}}:
                                    result += parse.table("".join(table))
                                case {'output_type': "stream", 'text': source}:
                                    if len(source) < 100:
                                        result += parse.output(source)
                                case {'output_type': "display_data", 'data': {'image/png': data}}:
                                    result += parse.image(output_path, data)

    with open(output_path + "/text.tex", 'w', encoding='utf-8') as f:
        f.write(result)





