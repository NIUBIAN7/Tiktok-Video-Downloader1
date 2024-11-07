import time
import pyperclip
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# 设置默认下载路径
DEFAULT_DOWNLOAD_PATH = "F:\\B_video"#需要自己修改为本地存储视频的文件夹位置
# 自动化无水印下载
def download_video(url, download_path=DEFAULT_DOWNLOAD_PATH):
    # 启动Edge浏览器
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    driver.get("https://tiksave.io/zh-cn#google_vignette")  # 打开下载网站

    # 粘贴视频链接并触发下载
    input_box = driver.find_element(By.XPATH, '//*[@id="s_input"]')  # 输入框的XPATH
    input_box.send_keys(url + Keys.RETURN)

    # 等待页面加载
    time.sleep(5)

    # 获取下载链接
    try:
        download_link = driver.find_element(By.XPATH, '//a[contains(@class, "tik-button-dl")]').get_attribute("href")
        if download_link:
            download_video_file(download_link, download_path)
            messagebox.showinfo("下载完成", f"视频已成功下载到 {download_path}！")
        else:
            messagebox.showwarning("下载失败", "未找到无水印下载链接")
    finally:
        driver.quit()

# 下载视频文件到指定本地文件夹
def download_video_file(video_url, download_path):
    os.makedirs(download_path, exist_ok=True)  # 确保目录存在
    # 使用时间戳生成唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(download_path, f"downloaded_video_{timestamp}.mp4")

    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
    else:
        messagebox.showerror("下载失败", "视频下载失败，请检查链接或网络连接。")

# GUI设计
def create_gui():
    # 初始化窗口
    root = tk.Tk()
    root.title("TikTok Video Downloader")
    root.geometry("400x200")

    # 标题标签
    label = tk.Label(root, text="请输入TikTok视频链接：")
    label.pack(pady=10)

    # 输入框
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=5)

    # 下载按钮
    download_button = tk.Button(root, text="下载视频", command=lambda: start_download(url_entry.get()))
    download_button.pack(pady=20)

    # 从剪贴板获取链接按钮
    clipboard_button = tk.Button(root, text="从剪贴板粘贴链接", command=lambda: paste_from_clipboard(url_entry))
    clipboard_button.pack()

    root.mainloop()

# 启动下载
def start_download(url):
    if "tiktok.com" in url:
        download_video(url)
    else:
        messagebox.showwarning("无效链接", "请输入有效的TikTok视频链接。")

# 从剪贴板粘贴链接到输入框
def paste_from_clipboard(entry):
    entry.delete(0, tk.END)
    entry.insert(0, pyperclip.paste())

# 主程序入口
if __name__ == "__main__":
    create_gui()
