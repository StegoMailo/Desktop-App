import requests

url = "https://sms77io.p.rapidapi.com/sms"

payload = {
	"to": "+970568466854",
	"p": "1c553b3D089A1d159131CEd724BD0905Cf68d88D48a46cd51Dc85B36238561B8",
	"text": "Dear customerxt order!"
}
headers = {
	"content-type": "application/x-www-form-urlencoded",
	"X-RapidAPI-Key": "db5eff21b5mshaca5e35f37c3aefp1c1da5jsne59cf4e70057",
	"X-RapidAPI-Host": "sms77io.p.rapidapi.com"
}

response = requests.post(url, data=payload, headers=headers)

print(response.json())