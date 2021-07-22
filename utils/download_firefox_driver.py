"""
download firefoxdriver
需要requests包
手动修改
  1、firefoxdriver_path=包下载绝对路径
  2、max_work_thread=工作线程数，通常等于cpu支持线程数

"""
import re
import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed, wait

chromedriver_path = 'E:/browser_driver/firefoxdriver/'
max_work_thread = 4


def _get_html_text(url: str) -> requests.Response.text:
    rsp = requests.get(url)
    if not rsp:
        raise ValueError('No Data Return!')
    return rsp.text


def extract_version_url(url='https://npm.taobao.org/mirrors/geckodriver'):
    html_text = _get_html_text(url)
    pattern = r'<a href=\"/mirrors/geckodriver/.*>(.*)/</a>'
    version_list = re.findall(pattern, html_text)
    download_url_list = [url + '/' + i + '/' for i in version_list]
    return download_url_list


def extract_download_url(url):
    html_text = _get_html_text(url)
    pattern = r'<a href=\"(/mirrors/geckodriver/.*/geckodriver.*)\">'
    download_url_list = ['https://npm.taobao.org' + url for url in re.findall(pattern, html_text)]
    return download_url_list


def download_zip(download_url: str, cover=False):
    def _download():
        rsp = requests.get(download_url)
        if not rsp:
            raise ValueError('No Data Return!')
        with open(file_abs_name, 'wb') as f:
            f.write(rsp.content)

    file_dir, file_name = tuple(download_url.split('/')[5:7])

    file_abs_dir = chromedriver_path + file_dir
    file_abs_name = file_abs_dir + '/' + file_name

    if not os.path.exists(file_abs_dir):
        os.makedirs(file_abs_dir, exist_ok=True)

    if not os.path.exists(file_abs_name):
        _download()
    elif cover:
        os.remove(file_abs_name)
        _download()
    else:
        """文件存在且不覆盖，直接return"""
        return


def run():
    executor = ThreadPoolExecutor(max_workers=max_work_thread)
    download_url_list = []
    t1 = time.time()
    version_url_list = extract_version_url()
    t2 = time.time()
    print(f'获取全部版本url时间为: {t2 - t1}')
    all_task = [executor.submit(extract_download_url, url) for url in version_url_list]
    for future in as_completed(all_task):
        url_list = future.result()
        download_url_list += url_list

    wait(all_task)
    t3 = time.time()
    print(f'获取所有zip包的下载url时间为： {t3 - t2}')
    all_tasks = [executor.submit(download_zip, url) for url in download_url_list]
    print('下载中，请等待。。。')
    count = 0
    for future in as_completed(all_tasks):
        if future.done():
            count += 1
            print(f'完成进度: {(count / len(download_url_list)):.2%}', flush=True)
    t4 = time.time()
    print(f'下载完成，总耗时: {t4 - t3}')
    print(f'总运行时间: {t4 - t1}')


if __name__ == '__main__':
    run()