import subprocess
import os
import shutil
import xml.etree.ElementTree as ET

def delete_directory(directory_path):
    try:
        shutil.rmtree(directory_path)
        print(f"目录 {directory_path} 已成功删除。")
    except OSError as e:
        print(f"删除目录 {directory_path} 时出错: {e}")

def manage_directory(directory_path):
    # 判断目录是否存在
    if os.path.exists(directory_path):
        print(f"目录 {directory_path} 已存在。")
    else:
        try:
            # 创建目录
            os.makedirs(directory_path)
            print(f"目录 {directory_path} 创建成功。")
        except OSError as e:
            print(f"创建目录 {directory_path} 失败，错误信息：{e}")


def clone_repo(repo_url, branch, github_path):
    subprocess.run(["git", "clone", repo_url, '-b', branch], cwd=github_path)


def get_submodule_revision(submodule_path):
    return subprocess.run(["git", "submodule", "status"], cwd=submodule_path, text=True, capture_output=True)


def parse_xml_from_file_etree(file_path, res_dict):
    tree = ET.parse(file_path)
    root = tree.getroot()
    for child in root:
        if child.tag == "project":
            if child.attrib.get("path") in res_dict:
                if child.attrib.get("revision") != res_dict.get(child.attrib.get("path")):
                    print("difference path:", child.attrib.get("path"))


def string_to_dict(input_string):
    result = {}
    lines = input_string.strip().split('\n')
    for line in lines:
        parts = line.strip().split(' ')
        if len(parts) == 2:
            # 提取 commit hash 和 repo name
            commit_hash = parts[0].strip('-')
            repo_name = parts[1].strip()
            result[repo_name] = commit_hash
    return result


def main():
    github_base_url = "git@github.com:"
    branch = "v0.0.0.163"
    sdk_name = "sdk.git"
    sdk_ucc_name = "sdk-ucc.git"
    public_url_prefix = "syna-astra-test/"
    public_test_prefix = "syna-astra-test/"
    stage_prefix = "syna-astra-stage/"
    ci_snapshot_file_file = "snapshot_syna-sdk-sirius_202501162218.xml"
    xml_dict = {}
    git_dict = {
        "sdk":{
            # "public" : github_base_url+public_url_prefix+sdk_name,
            "public-test" : github_base_url+public_test_prefix+sdk_name,
            "stage" : github_base_url+stage_prefix+sdk_name,
        },
        "sdk-ucc":{
            # "public" : github_base_url+public_url_prefix+sdk_ucc_name,
            "public-test" : github_base_url+public_test_prefix+sdk_ucc_name,
            "stage" : github_base_url+stage_prefix+sdk_ucc_name,
        }
    }

    submodules = ""
    for k,v in git_dict.items():
        delete_directory(k)
        manage_directory(k)
        for github, repo_url in v.items():
            # print(repo_url)
            github_path = os.path.join(k, github)
            manage_directory(github_path)
            clone_repo(repo_url, branch, github_path)
            _submodules = get_submodule_revision(os.path.join(github_path, k))
            _submodules = _submodules.stdout
            if _submodules:
                if submodules != "" and submodules != _submodules:
                    print("path", os.path.join(github_path, k))
                submodules = _submodules

    res_dict = string_to_dict(submodules)
    parse_xml_from_file_etree(ci_snapshot_file_file, res_dict)

if __name__ == "__main__":
    main()