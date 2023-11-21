import difflib
import requests
from colorama import Fore, Style



# прописываем хосты окружения
hostDev = "https://bank.uralfd.farzoomplace.ru/"
hostProd = "http://longan-develop.boos.solutions/"
endpoints = ["api/doc-template/actuator/info", "api/bg-scoring/actuator/info", "pa/bg-pa/rev", "api/zgr-service/actuator/info", "api/svs/actuator/info", "api/abs/actuator/info", "api/bg-scoring/actuator/info", "pa/bg-pa-custom/rev", "api/limit/actuator/info", "api/process-integration/actuator/info", "docapi/actuator/info", "api/sas/actuator/info", "pa/bg-pa-commission-change/rev", "es/version/_search?pretty"]

for elements in endpoints:
# получаем страницу
    urlDev = hostDev + elements
    respDev = requests.get(urlDev)

    if "error" not in respDev.text:
# получаем данные страницы и сохраняем его в txt-файл
        with open("DevVersion.txt", "a") as f:
         f.write(elements + "\n")
         f.write(respDev.text + "\n")
# получаем данные страницы  и сохраняем его в другой txt-файл
    urlProd = hostProd + elements
    respProd = requests.get(urlProd)
    if "page not found" not in respProd.text:
        with open("ProdVersion.txt", "a") as f:
         f.write(elements + "\n")
         f.write(respProd.text + "\n")



# преобразуем содержимое txt-файлов в строки
with open("DevVersion.txt", "r") as f1, open("ProdVersion.txt", "r") as f2:
    content1 = f1.read()
    content2 = f2.read()

# сравниваем содержимое файлов и записываем различия в файл diff.txt
with open("diff.txt", "w") as f:
    if content1 == content2:
        f.write("Files are identical")
    else:
        diff = difflib.unified_diff(content1.splitlines(), content2.splitlines(), fromfile='DevVersion.txt', tofile='ProdVersion.txt')
        f.write('\n'.join(diff))

# открываем файл с различиями
with open("diff.txt", "r") as f:
    diff_content = f.readlines()

# выделяем измененные строки цветом
with open("diff_colored.txt", "w") as f:
    for line in diff_content:
        if line.startswith("+"):
            f.write(Fore.GREEN + line + Style.RESET_ALL)
        elif line.startswith("-"):
            f.write(Fore.RED + line + Style.RESET_ALL)
        else:
            f.write(line)