import logging, uuid, random
from locust import HttpUser, task, constant_throughput


class QuickstartUser(HttpUser):
    wait_time1 = constant_throughput(30)
    host = "http://172.27.176.7"

    @task(50)
    def get_stats(self):
        self.client.get("/api/getstat", name='Get Stats', verify=False)

    @task(50)
    def open_list_of_test_cases(self):
        self.client.get("/api/tests", name='Open list of Test Cases', verify=False)

    @task(10)
    def create_new_test_case(self):
        name = uuid.uuid4()
        description = uuid.uuid4()
        self.client.post("/api/tests/new", json={'name': f'test nr {name}', 'description': f'test nr {description}'},
                         name='Create new Test Case', verify=False)

    @task(10)
    def open_test_case_details(self):
        test_id = random.randint(1, 10)
        self.client.get(f'/api/tests/{test_id}', name='Open Test Case details', verify=False)

    @task(30)
    def change_test_case_status_to_pass(self):
        test_id = random.randint(1, 10)
        self.client.post(f'/api/tests/{test_id}/status', json={"status": "PASS"},
                         name='Change Test Case status to PASS', verify=False)

    @task(5)
    def update_test_case(self):
        test_id = random.randint(1, 10)
        name = uuid.uuid4()
        description = uuid.uuid4()
        self.client.put(f'/api/tests/{test_id}', json={'name': f'test nr {name}', 'description': f'test nr {description}'},
                         name='Update Test Case', verify=False)

    @task(5)
    def partial_update_test_case(self):
        test_id = random.randint(1, 10)
        name = uuid.uuid4()
        self.client.patch(f'/api/tests/{test_id}', json={'name': f'test nr {name}'},
                         name='Partial update Test Case', verify=False)

    @task(30)
    def change_test_case_status_to_fail(self):
        test_id = random.randint(1, 10)
        self.client.post(f'/api/tests/{test_id}/status', json={"status": "FAIL"},
                         name='Change Test Case status to FAIL', verify=False)

    def on_stop(self):
        self.client.post("/api/auth/logout", name='Logout', verify=False)

    def on_start(self):
        rs = self.client.post("/api/auth/login", json={"username": "bob", "password": "Qamania123"}, name='Login', verify=False)
        token = self.client.cookies.get('csrftoken')
        self.client.headers.update({'X-CSRFToken': token})
        # logging
        print(rs.request.body)
        logging.info('Token = ' + token)