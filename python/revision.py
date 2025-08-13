import subprocess
import os
import shutil
import xml.etree.ElementTree as ET
import glob
import urllib.request
import logging
import sys

def init_snapshot_manifest(url):
    function_name = sys._getframe().f_code.co_name
    # 获取当前目录下所有 .xml 文件
    xml_files = glob.glob("*.xml")

    # 遍历并删除每一个文件
    for xml_file in xml_files:
        try:
            os.remove(xml_file)
            logging.info(f"[{function_name}]已删除文件: {xml_file}")
        except OSError as e:
            logging.info(f"[{function_name}]删除文件失败 {xml_file}: {e}")

    try:
        filename = url.split('/')[-1]
        save_path = os.path.join(os.getcwd(), filename)
        logging.info(save_path)
        logging.info(f"[{function_name}] donwloading: {url} -> {save_path}")
        urllib.request.urlretrieve(url, save_path)
        logging.info(f"[{function_name}] ✅ file have been downloaded to: {save_path}")
    except Exception as e:
        logging.info(f"[{function_name}] ❌ download failed: {e}")


def delete_directory(directory_path):
    function_name = sys._getframe().f_code.co_name
    try:
        shutil.rmtree(directory_path)
        logging.info(f"[{function_name}]dir {directory_path} delete success.")
    except OSError as e:
        logging.error(f"[{function_name}]deleteing {directory_path} error: {e}")

def manage_directory(directory_path):
    function_name = sys._getframe().f_code.co_name
    # 判断目录是否存在
    if os.path.exists(directory_path):
        logging.info(f"[{function_name}]目录 {directory_path} 已存在。")
    else:
        try:
            # 创建目录
            os.makedirs(directory_path)
            logging.info(f"[{function_name}]目录 {directory_path} 创建成功。")
        except OSError as e:
            logging.error(f"[{function_name}]创建目录 {directory_path} 失败，错误信息：{e}")


def clone_repo(repo_url, branch_name, github_path):
    result = subprocess.run(["git", "clone", repo_url, '-b', branch_name], cwd=github_path)
    return result

def get_submodule_revision(submodule_path):
    return subprocess.run(["git", "submodule", "status"], cwd=submodule_path, text=True, capture_output=True)


def parse_xml_from_file_etree(file_path, res_dict):
    function_name = sys._getframe().f_code.co_name
    difference = False
    tree = ET.parse(file_path)
    root = tree.getroot()
    for child in root:
        if child.tag == "project":
            if child.attrib.get("path") in res_dict:
                if child.attrib.get("revision") != res_dict.get(child.attrib.get("path")):
                    difference = True
                    logging.info("difference path:", child.attrib.get("path"))
    if difference is False:
        logging.info(f"[{function_name}] comparison results are consistent")


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


def main(ci_snapshot_file_url, branch_name):
    function_name = sys._getframe().f_code.co_name
    github_base_url = "git@github.com:"
    # branch_name = "kirkstone_5.15_v1.7.0.50"
    sdk_name = "sdk.git"
    sdk_ucc_name = "sdk-ucc.git"
    public_url_prefix = "synaptics-astra/"
    public_test_prefix = "syna-astra-test/"
    stage_prefix = "syna-astra-stage/"
    res_dict = {}
    # ci_snapshot_file_url = 'http://iotmmswfileserver.synaptics.com:8000/sandal/Firebird/202508/20250811/202508112018/snapshot_syna-sdk-sirius_202508112018.xml'
    ci_snapshot_file_file = ci_snapshot_file_url.split('/')[-1]
    git_dict = {
        "sdk":{
            "public" : github_base_url+public_url_prefix+sdk_name,
            "public-test" : github_base_url+public_test_prefix+sdk_name,
            "stage" : github_base_url+stage_prefix+sdk_name,
        },
        "sdk-ucc":{
            "public" : github_base_url+public_url_prefix+sdk_ucc_name,
            "public-test" : github_base_url+public_test_prefix+sdk_ucc_name,
            "stage" : github_base_url+stage_prefix+sdk_ucc_name,
        }
    }

    submodules = ""
    for k,v in git_dict.items():
        delete_directory(k)
        manage_directory(k)
        for github, repo_url in v.items():
            github_path = os.path.join(k, github)
            manage_directory(github_path)
            result = clone_repo(repo_url, branch_name, github_path)
            if result.returncode == 128:
                logging.info(f"[{function_name}]{repo_url} continue")
                continue
            _submodules = get_submodule_revision(os.path.join(github_path, k))
            _submodules = _submodules.stdout
            if _submodules:
                if submodules != "" and submodules != _submodules:
                    logging.info("path", os.path.join(github_path, k))
                submodules = _submodules
    res_dict = string_to_dict(submodules)
    logging.info(f"[{function_name}]res_dict {res_dict}")
    init_snapshot_manifest(ci_snapshot_file_url)

    if len(res_dict) != 0:
        parse_xml_from_file_etree(ci_snapshot_file_file, res_dict)

if __name__ == "__main__":
    ci_snapshot_file_url = input("input ci_snapshot_file_url: ")
    branch_name = input("input branch_name: ")
    main(ci_snapshot_file_url, branch_name)