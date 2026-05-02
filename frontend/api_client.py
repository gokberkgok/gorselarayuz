"""
API Client — Wraps all HTTP calls to the FastAPI backend.
"""
import requests
from typing import Optional


class ApiClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.user_id: Optional[int] = None
        self.user_name: Optional[str] = None
        self.user_role: Optional[str] = None

    def _h(self):
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _u(self, p): return f"{self.base_url}{p}"

    def _r(self, resp):
        if resp.status_code >= 400:
            try: detail = resp.json().get("detail", resp.text)
            except: detail = resp.text
            raise Exception(f"API Error ({resp.status_code}): {detail}")
        return resp.json() if resp.text else {}

    def login(self, email, password):
        d = self._r(requests.post(self._u("/auth/login"), json={"email": email, "password": password}))
        self.token, self.user_id, self.user_name, self.user_role = d["access_token"], d["user_id"], d["name"], d["role"]
        return d

    def register(self, name, email, password):
        d = self._r(requests.post(self._u("/auth/register"), json={"name": name, "email": email, "password": password}))
        self.token, self.user_id, self.user_name, self.user_role = d["access_token"], d["user_id"], d["name"], d["role"]
        return d

    def get_me(self):
        return self._r(requests.get(self._u("/auth/me"), headers=self._h()))

    def logout(self):
        self.token = self.user_id = self.user_name = self.user_role = None

    def get_types(self):
        return self._r(requests.get(self._u("/types"), headers=self._h()))

    def create_type(self, name):
        return self._r(requests.post(self._u("/types"), json={"name": name}, headers=self._h()))

    def get_places(self, type_id=None, search=None, skip=0, limit=20):
        p = {"skip": skip, "limit": limit}
        if type_id: p["type_id"] = type_id
        if search: p["search"] = search
        return self._r(requests.get(self._u("/places"), params=p, headers=self._h()))

    def get_random_places(self, count=5):
        return self._r(requests.get(self._u("/places/random"), params={"count": count}, headers=self._h()))

    def create_place(self, name, type_id, description="", image_url=""):
        return self._r(requests.post(self._u("/places"), json={"name": name, "type_id": type_id, "description": description, "image_url": image_url}, headers=self._h()))

    def update_place(self, place_id, **kw):
        return self._r(requests.put(self._u(f"/places/{place_id}"), json=kw, headers=self._h()))

    def delete_place(self, place_id):
        return self._r(requests.delete(self._u(f"/places/{place_id}"), headers=self._h()))

    def create_reservation(self, place_id, date, start_time, end_time):
        return self._r(requests.post(self._u("/reservations"), json={"place_id": place_id, "date": date, "start_time": start_time, "end_time": end_time}, headers=self._h()))

    def get_my_reservations(self):
        return self._r(requests.get(self._u("/reservations/my"), headers=self._h()))

    def cancel_reservation(self, rid):
        return self._r(requests.put(self._u(f"/reservations/{rid}/cancel"), headers=self._h()))

    def get_all_reservations(self, status_filter=None):
        p = {}
        if status_filter: p["status_filter"] = status_filter
        return self._r(requests.get(self._u("/reservations/all"), params=p, headers=self._h()))

    def approve_reservation(self, rid):
        return self._r(requests.put(self._u(f"/reservations/{rid}/approve"), headers=self._h()))

    def reject_reservation(self, rid):
        return self._r(requests.put(self._u(f"/reservations/{rid}/reject"), headers=self._h()))

    def get_stats(self):
        return self._r(requests.get(self._u("/reservations/stats"), headers=self._h()))
