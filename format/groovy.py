import re

def format_function_parameters(file_path, new_file_path, mode = 1):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 匹配 Groovy 函数定义
    match mode:
        case 0:
            pattern = re.compile(r'(\b(?:def|static|public|private|protected)\s+[a-zA-Z_$][a-zA-Z0-9_$]*\s*\()([^)]*\))')
        case 1:
            pattern = re.compile(r"'buildTemplate' :.*?\)")
        case _:
            print("It's not supported for the time being")
            return
    new_content = ""
    pos = 0
    for match in pattern.finditer(content):
        print(match)
        start, end = match.span()
        new_content += content[pos:start]
        func_start, params = match.groups()

        # 处理参数部分
        formatted_params = []
        current_line = ""
        first_for = True
        for param in params.strip('()').split(','):
            print("param", param)
            param = param.strip()
            # print("param", len(current_line + (',' if current_line else '')) + len(func_start))
            if len(current_line + (',' if current_line else '')) + len(func_start) > 130 and first_for:
                first_for = False
                if current_line:
                    formatted_params.append(current_line + ",")
                current_line = ' ' * len(func_start) + param
            else:
                if current_line:
                    current_line += ', '
                current_line += param
        if current_line:
            formatted_params.append(current_line)

        # 重新组合函数定义
        new_params = '\n'.join(formatted_params)
        new_function = f"{func_start}{new_params})"
        new_content += new_function
        pos = end
        # print(new_function)
    new_content += content[pos:]

    # 将处理后的内容写回文件
    if new_file_path:
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print("The writting of the new file has been completed")

# 使用示例
file_path = 'test.txt'
new_file_path = 'test.groovy'
format_function_parameters(file_path, None, 1)