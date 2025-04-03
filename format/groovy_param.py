def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print("The writting of the new file has been completed")


def delete_space(line, new_content, index):
    if index != 8:
        if line[:index].startswith("  "):
            new_line = line[:index - 4] + line[index:]
            new_content = new_content + new_line + '\n'
        else:
            new_content = new_content + line + '\n'
    else:
        new_content = new_content + line + '\n'
    return new_content


# 把每行缩短多余的参数放到下一行
def deal_with_line(line, line_len_limit, new_content):
    line_len = line.__len__()
    if line_len > line_len_limit:
        line_split = line.split(",")
        current_line = ""
        new_line = []
        for item in line_split:
            if len(current_line) < line_len_limit:
                current_line = current_line + item + ","
            else:
                new_line.append(current_line)
                current_line = " " * 24 + item + ","
            # print(current_line)
        new_line.append(current_line)
        # print(new_line)
        new_content = new_content + "\n".join(new_line) + "\n"
    else:
        new_content = new_content + line + '\n'

    return new_content


def deal_with_content(content, find_index, line_len_limit):
    new_content = ""
    for line in content.splitlines():
        add = True
        for item in find_index:
            index = line.find(item)
            if index != -1:
                # new_content = delete_space(line, new_content, index)
                new_content = deal_with_line(line, line_len_limit, new_content)
                add = False
                break
        if add:
            new_content = new_content + line + '\n'

    return new_content

if __name__ == "__main__":
    # find_index = ["'buildTemplate'", "'resultDir'", "'version'", "'OS'"]
    find_index = ["'buildTemplate'"]
    new_path = "test.groovy"
    file_path = "test.txt"
    # file_path = "text.groovy"
    line_len_limit = 130
    content = read_file(file_path)
    new_content = deal_with_content(content, find_index, line_len_limit)
    write_file(new_path, new_content)
