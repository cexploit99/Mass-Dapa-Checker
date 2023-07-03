import requests
from bs4 import BeautifulSoup
import json

file_path = input("Input file domain (.txt): ")
with open(file_path, "r") as file:
    domains = [line.strip() for line in file.readlines()]

results = []
for domain in domains:
    url = "https://tools.cx99.my.id/tools/checker/cekda.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4593.122 Safari/537.36"
    }
    data = {
        "url_form": domain
    }

    response = requests.post(url, headers=headers, data=data)
    server_output = response.text

    if response.status_code != 200:
        error_msg = response.text
        # print(f"Error: {error_msg}")
        print(f"Error: Request To Server Api Error!")
        continue

    dom = BeautifulSoup(server_output, 'html.parser')
    tables = dom.find_all('table')

    resultsda = []
    resultspa = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                da = f"{cols[2].text}"
                resultsda.append(da)
                pa = f"{cols[3].text}"
                resultspa.append(pa)

    if len(resultsda) > 0 and len(resultspa) > 0:
        result = {
            'domain': domain,
            'DA': resultsda[0],
            'PA': resultspa[0]
        }
        results.append(result)

        print(f"Domain: {result['domain']}")
        print(f"DA: {result['DA']}")
        print(f"PA: {result['PA']}")
        print()
    else:
        print(f"No data found for domain: {domain}")
        print()

output_file_path = "dapachecker.txt"
with open(output_file_path, "w") as output_file:
    for result in results:
        output_file.write(f"Domain: {result['domain']}\n")
        output_file.write(f"DA: {result['DA']}\n")
        output_file.write(f"PA: {result['PA']}\n")
        output_file.write("\n")

print(f"Hasil pengecekan telah disimpan dalam file: {output_file_path}")
