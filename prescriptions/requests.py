import requests


class Request:

    def __init__(self):
        self.uri = "https://mock-api-challenge.dev.iclinic.com.br/"
        self.bearer = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJzZXJ2aWNlIjoicGh5c2ljaWFucyJ9.Ei58MtFFGBK4uzpxwnzLxG0Ljdd-NQKVcOXIS4UYJtA"

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

        except requests.exceptions.HTTPError as err:
            print(str(err))
            raise Exception(err)
        except Exception as e:
            print(str(e))
            raise Exception(e)

    def request_physicians(self, id_phy):
        try:
            response = requests.get(
                self.uri + f'physicians/{id_phy}/',
                headers={
                    'cache-control': 'no-cache',
                    'Authorization': f'Bearer {self.bearer}',
                }
            )
            payload = response.json()

            return payload

        except requests.exceptions.HTTPError as err:
            print(str(err))
            raise Exception(err)
        except Exception as e:
            print(str(e))
            raise Exception(e)