import requests
from .mocks.data import MOCK_DATA


class Request:
    def __init__(self):
        self.uri = "mock://"  # mantido por compatibilidade
        self.malformed = {
            "error": {
                "code": "01",
                "message": 'malformed request'
            }
        }

    def request_metrics(self, metrics):
        try:
            return MOCK_DATA["metrics"]
        except KeyError:
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
            physician = MOCK_DATA["physicians"].get(id_phy)
            if not physician:
                return {
                    "error": {
                        "code": "02",
                        "message": 'physician not found'
                    }
                }, True
            return physician, False
        except KeyError:
            raise {
                "error": {
                    "code": "05",
                    "message": 'physicians service not available'
                }
            }
        except Exception:
            raise self.malformed

    def request_clinics(self, id_clinic):
        try:
            clinic = MOCK_DATA["clinics"].get(id_clinic)
            if not clinic:
                return {
                    "error": {
                        "code": "07",
                        "message": 'clinic not found'
                    }
                }, True
            return clinic, False
        except KeyError:
            raise {
                "error": {
                    "code": "08",
                    "message": 'clinics service not available'
                }
            }
        except Exception:
            raise self.malformed

    def request_patients(self, id_patient):
        try:
            patient = MOCK_DATA["patients"].get(id_patient)
            if not patient:
                return {
                    "error": {
                        "code": "03",
                        "message": 'patient not found'
                    }
                }, True
            return patient, False
        except KeyError:
            raise {
                "error": {
                    "code": "06",
                    "message": 'patients service not available'
                }
            }
        except Exception:
            raise self.malformed
