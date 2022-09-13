import urllib3
import wget
from pathlib import Path
from tqdm import tqdm

status_list = []
download_list = []
download_path = Path.home() / "Worksheets"
download_path.mkdir(parents=True, exist_ok=True)
print(download_path)

for i in tqdm(range(1000)):
    path = f"https://cls.nus.edu.sg/nusgerman/data/course_path/{i}.pdf"
    # print(path)
    http = urllib3.PoolManager()
    r = http.request('GET', path)
    # print(r.status)
    status_list = status_list + [r.status]
    if r.status == 200:
        wget.download(path, str(download_path))
        download_list.append(i)

print(set(status_list))
print(download_list)
