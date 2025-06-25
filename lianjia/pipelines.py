import csv

class LianjiaPipeline:
    def open_spider(self, spider):
        try:
            self.file = open('lianjia_sh_jinshan.csv', 'w', newline='', encoding='utf-8-sig')
            self.writer = None
        except Exception as e:
            print(f"[ERROR] 打开文件失败: {e}")

    def process_item(self, item, spider):
        item_dict = dict(item)
        if self.writer is None:
            fieldnames = list(item_dict.keys())
            self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
            self.writer.writeheader()

        self.writer.writerow(item_dict)
        return item

    def close_spider(self, spider):
        self.file.close()
