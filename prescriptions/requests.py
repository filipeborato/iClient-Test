import requests


class Request:

    def __init__(self):
        self.uri = "https://mock-api-challenge.dev.iclinic.com.br/"
        self.malformed = {
            "error": {
                "code": "01",
                "message": 'malformed request'
            }
        }

    def request_metrics(self, metrics):
        try:
            response = requests.post(
                self.uri + 'metrics/',
                data=metrics,
                headers={
                    'cache-control': 'no-cache',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Bearer SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
                }
            )

            payload = response.json()

            return payload

        except requests.exceptions.HTTPError:
            raise {
                "error": {
                    "code": "04",
                    "message": 'metrics service not available'
                }
            }

        except Exception:
            raise self.malformed

    def request_physicians(self, id_phy):
        try:
            response = requests.get(
                self.uri + f'physicians/{id_phy}/',
                headers={
                    'cache-control': 'no-cache',
                    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA',
                }
            )
            payload = response.json()

            if 'detail' in payload:
                return {
                           "error": {
                               "code": "02",
                               "message": 'physician not found'
                           }
                       }, True

            return payload, False

        except requests.exceptions.HTTPError:
            raise {
                "error": {
                    "code": "05",
                    "message": 'physicians service not availabled'
                }
            }

        except Exception:
            raise self.malformed

    def request_clinics(self, id_clinic):
        try:
            response = requests.get(
                self.uri + f'clinics/{id_clinic}/',
                headers={
                    'cache-control': 'no-cache',
                    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoiY2xpbmljcyJ9.r3w8KS4LfkKqZhOUK8YnIdLhVGJEqnReSClLCMBIJRQ',
                }
            )
            payload = response.json()

            if 'detail' in payload:
                return {
                    "error": {
                        "code": "07",
                        "message": 'clinic not found'
                    }
                }, True

            return payload, False

        except requests.exceptions.HTTPError:
            raise {
                "error": {
                    "code": "08",
                    "message": 'patients service not available'
                }
            }

        except Exception:
            raise self.malformed

    def request_patients(self, id_patient):
        try:
            response = requests.get(
                self.uri + f'patients/{id_patient}/',
                headers={
                    'cache-control': 'no-cache',
                    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGF0aWVudHMifQ.Pr6Z58GzNRtjX8Y09hEBzl7dluxsGiaxGlfzdaphzVU',
                }
            )
            payload = response.json()

            if 'detail' in payload:
                return {
                           "error": {
                               "code": "03",
                               "message": 'patient not found'
                           }
                       }, True

            return payload, False

        except requests.exceptions.HTTPError as err:
            raise {
                "error": {
                    "code": "06",
                    "message": 'patients service not available'
                }
            }

        except Exception:
            raise self.malformed
