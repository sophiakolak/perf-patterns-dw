import requests
from html.parser import HTMLParser
import regex
import json
from ast import literal_eval

class HTMLParser(HTMLParser):
    def handle_data(self, data):
        if "var pageData" in data:
            pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')             
            js_obj = pattern.findall(data)[0].encode().decode('unicode-escape')
            lines = js_obj.splitlines()
            for js in lines:
                if 'runtimeDistribution' in js: 
                    pattern = regex.compile(r'\[(.*)\]')
                    a = pattern.findall(js)[0].replace("\"", "")
                    self.data = list(literal_eval(a))

    '''
    Note: These cookies will expire after 14 days and were specific to the account we used
    '''
    def define_headers():
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "cookie": "__cfduid=d54493c5a593789f464efa0e9f2329aa51604155525; __cf_bm=1735af4b07d7f392aa571f0d2a3b3db4d582258b-1604155525-1800-ARtu/7bW6bIY5SOiVgGYCllIderDVQFAI+GMeIJXnGqoCPr7i+yWuHob9mSXP0HSXY2opCt9Ie0ZYmZ6mKU5M6U=; csrftoken=D1kDxnggpG56mUgHtO9UX4wyXB5yvI9uu10FFuDQqEtcTnQ7fwnMRE8FJBMWODmQ; messages=\"653c35088e484ab69d9d7bdebb0635f59766dbf5$[[\\\"__json_message\\\"\\0540\\05425\\054\\\"Successfully signed in as rkrsn.\\\"]]\"; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTA1MDA2NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImNmMDAzYzY2MjFiY2MyNjNmNjNmZDc1NWJjYjg5YzY1OTAyZjI1NzMiLCJpZCI6MTA1MDA2NiwiZW1haWwiOiJpLm0ucmFsa0BnbWFpbC5jb20iLCJ1c2VybmFtZSI6InJrcnNuIiwidXNlcl9zbHVnIjoicmtyc24iLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvaW1yYWxrL2F2YXRhcl8xNTIxNzQ2NjE1LnBuZyIsInJlZnJlc2hlZF9hdCI6MTYwNDE1NTY3NSwiaXAiOiI3My44OC4yMzUuMzEiLCJpZGVudGl0eSI6IjNhMzlhMWQ2NjEzNzgyM2YzNjdkMDQ4Mjk0MGJkN2I4Iiwic2Vzc2lvbl9pZCI6MzU5NjcxNiwiX3Nlc3Npb25fZXhwaXJ5IjoxMjA5NjAwfQ.vVpsgd7xM7wpcR8q3IKFdiU8rdqHzfMzCnyFInCXh0s",
            "referrer": "https://leetcode.com/accounts/login/?next=/submissions/detail/182745087/",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "body": None,
            "method": "GET",
            "mode": "cors"
        }

        cookie = "__cfduid=d58b6e3025ee9256e0ee64065cd37759a1604153947; csrftoken=HWIgFBvmIabUpnyqyezsXow1SJoPh9WNy5Zmsd0fdeaGp2A3vn4vpmQeKY8fVTZu; _ga=GA1.2.582641511.1604153949; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTA1MDA2NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImZhZjMxYzM2NzcxZGUxOGU5NDg3MTMxM2U3ODYwYTljZTRiYzZmNmIiLCJpZCI6MTA1MDA2NiwiZW1haWwiOiJpLm0ucmFsa0BnbWFpbC5jb20iLCJ1c2VybmFtZSI6InJrcnNuIiwidXNlcl9zbHVnIjoicmtyc24iLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvaW1yYWxrL2F2YXRhcl8xNTIxNzQ2NjE1LnBuZyIsInJlZnJlc2hlZF9hdCI6MTYwNDMyOTcxNywiaXAiOiIxODQuMTUyLjMuMTE3IiwiaWRlbnRpdHkiOiJiY2EwOTA4OTg2OWEwMzEwYmYxZDIzZDY1Y2ViYjhkNCIsInNlc3Npb25faWQiOjM2NzE2NDksIl9zZXNzaW9uX2V4cGlyeSI6MTIwOTYwMH0._mwX75DocZCrCmcf6hjQ4fLOKIDNSt-zmgjqNmy7BWA; __atuvc=1%7C44%2C2%7C45; _gid=GA1.2.2107147145.1604329711; messages=\"653c35088e484ab69d9d7bdebb0635f59766dbf5$[[\\\"__json_message\\\"\\0540\\05425\\054\\\"Successfully signed in as rkrsn.\\\"]]\"; __cf_bm=4bad1b8b02a6b004c21502fc0bd3f45a1505eccc-1604332001-1800-AasTXvapxocXTSbxYN5oCRMCeQOsaZtIvRurIQPP+EJRl1jC6GCz+UagQmj12AzRjK+XazAyFiggTYzAn7Sm2K8=; c_a_u=\"cmtyc24=:1kZc32:33yZjmBNMtiOkEB4ZQozd--vjGc\"; __atuvs=5fa02a04b4b7e60b000"
        headers["cookie"] = cookie

        return headers



