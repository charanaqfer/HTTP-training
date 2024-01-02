import requests

response=requests.get("https://c006.preprod.aqfer.net/1/a/c.gif",allow_redirects=False)

# print(response.status_code)
# print(response.url)
print(response.headers)
# print(response.text)
print(response)

# for i,j in response.headers.items():
#     print(i,j)
# print("Hello")