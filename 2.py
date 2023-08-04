import tkinter as tk
from tkinter import ttk
import requests
import urllib.parse
import execjs
import csv
from concurrent.futures import ThreadPoolExecutor
from tkinter import filedialog

class BaiduIndexTool:
    def __init__(self, window):
        self.window = window
        self.window.title("百度指数查询工具")

        # 创建输入框和标签
        self.import_button = ttk.Button(window, text="导入关键词", command=self.import_keywords)
        self.import_button.grid(row=0, column=0, padx=5, pady=5)
        self.keyword_var = tk.StringVar()
        self.keyword_entry = ttk.Entry(window, textvariable=self.keyword_var)
        self.keyword_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        self.area_label = ttk.Label(window, text="地区:")
        self.area_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.area_var = tk.StringVar()
        self.area_combobox = ttk.Combobox(window, textvariable=self.area_var)
        self.area_combobox.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        self.area_combobox['values'] = ['山东', '贵州', '江西', '重庆', '内蒙古', '湖北', '辽宁', '湖南', '福建', '上海', '北京', '广西', '广东',
                                        '四川', '云南', '江苏', '浙江', '青海', '宁夏', '河北', '黑龙江', '吉林', '天津', '陕西', '甘肃',
                                        '新疆', '河南', '安徽', '山西', '海南', '台湾', '西藏', '香港', '澳门']

        self.start_date_label = ttk.Label(window, text="开始日期:")
        self.start_date_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_date_var = tk.StringVar()
        self.start_date_entry = ttk.Entry(window, textvariable=self.start_date_var)
        self.start_date_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        self.end_date_label = ttk.Label(window, text="结束日期:")
        self.end_date_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.end_date_var = tk.StringVar()
        self.end_date_entry = ttk.Entry(window, textvariable=self.end_date_var)
        self.end_date_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        self.cookie_label = ttk.Label(window, text="Cookie:")
        self.cookie_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.cookie_var = tk.StringVar()
        self.cookie_entry = ttk.Entry(window, textvariable=self.cookie_var)
        self.cookie_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        self.user_agent_label = ttk.Label(window, text="User-Agent:")
        self.user_agent_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.user_agent_var = tk.StringVar()
        self.user_agent_entry = ttk.Entry(window, textvariable=self.user_agent_var)
        self.user_agent_entry.grid(row=5, column=1, columnspan=2, padx=5, pady=5)

        self.cipher_text_label = ttk.Label(window, text="Cipher-Text:")
        self.cipher_text_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.cipher_text_var = tk.StringVar()
        self.cipher_text_entry = ttk.Entry(window, textvariable=self.cipher_text_var)
        self.cipher_text_entry.grid(row=6, column=1, columnspan=2, padx=5, pady=5)

        # 创建按钮
        self.query_button = ttk.Button(window, text="查询", command=self.query_baidu_index)
        self.query_button.grid(row=7, column=0, padx=5, pady=5)

        self.export_button = ttk.Button(window, text="导出数据", command=self.export_data)
        self.export_button.grid(row=7, column=1, padx=5, pady=5)

        self.result_text = tk.Text(window, width=50, height=20)
        self.result_text.grid(row=8, column=0, columnspan=3, padx=5, pady=5)

    def import_keywords(self):
        file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        if file_path:
            with open(file_path, 'r') as file:
                keywords = file.read()
                self.keyword_var.set(keywords)

    def query_baidu_index(self):
        keyword_input = self.keyword_var.get()
        keywords = keyword_input.split(',')
        if len(keywords) == 1 and keywords[0].endswith('.txt'):
            with open(keywords[0], 'r') as file:
                keywords = file.read().splitlines()
        area = self.area_var.get()
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        cookie = self.cookie_var.get()
        user_agent = self.user_agent_var.get()
        cipher_text = self.cipher_text_var.get()
        baseUrl = 'https://index.baidu.com/api/SearchApi/index'
        headers = {
            'Referer': 'https://index.baidu.com/v2/main/index.html',
            'Cookie': cookie,
            'User-Agent': user_agent,
            'Cipher-Text': cipher_text
        }

        all_results = {}  # 使用字典存储所有查询结果，关键词作为键，查询结果作为值
        for keyword in keywords:
            addUrl = f'?area={area}&word=[[%7B%22name%22:%22{urllib.parse.quote(keyword.strip())}%22,%22wordType%22:1%7D]]&startDate={start_date}&endDate={end_date}'
            res = requests.get(url=baseUrl + addUrl, headers=headers).json()

            if 'data' in res:
                all_data = res['data']['userIndexes'][0]['all']['data']
                uniqid = res['data']['uniqid']
                url = 'https://index.baidu.com/Interface/ptbk?uniqid=' + uniqid
                res = requests.get(url=url, headers=headers).json()
                cipher_data = res['data']
                ctx = execjs.compile(
                    'var decrypt=function(t, e) {if (!t) return "";for (var a = t.split(""), n = e.split(""), i = {}, r = [], o = 0; o < a.length / 2; o++) i[a[o]] = a[a.length / 2 + o];for (var s = 0; s < e.length; s++) r.push(i[n[s]]);return r.join("")}')
                result_data = ctx.call('decrypt', cipher_data, all_data)
                all_results[keyword] = result_data  # 将关键词和对应结果加入结果字典
            else:
                all_results[keyword] = "查询失败，请检查参数或稍后重试。"

        self.result_text.delete(1.0, tk.END)
        for keyword, result_data in all_results.items():
            self.result_text.insert(tk.END, f'Result Data for "{keyword}": {result_data}\n')

    def export_data(self):
        result_data = self.result_text.get(1.0, tk.END).strip()

        if not result_data:
            self.show_error("没有查询结果，无法导出。")
            return

        file_path = "baidu_index_data.csv"
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Keyword", "Index Data"])
            for line in result_data.split("\n"):
                keyword, index_data = line.split(": ", 1)
                writer.writerow([keyword, index_data])

    def show_error(self, message):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message, "error")

if __name__ == "__main__":
    window = tk.Tk()
    tool = BaiduIndexTool(window)
    window.mainloop()
