from django.test import TestCase

# Create your tests here.


import requests



res=requests.get("https://www.jd.com/?",params={"keyword":"美女"})
print(res.text)

with open('jd.html',"wb") as f:
    f.write(res.content)
