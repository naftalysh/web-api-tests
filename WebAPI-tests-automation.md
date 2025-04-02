### **Simulation System to Define, Design, and Implement a Web Application Testing Solution with API Tests**

**Objective:**  
Develop a complete simulation system to define, design, and implement a web application testing solution that includes:  
1. **API Testing** using `pytest`  
2. **Performance Testing**  
3. **Integration with GitHub Actions CI/CD**  
4. **Application running on a Kubernetes cluster** using **MongoDB** as the database  
5. **Comprehensive reporting** with multiple alternative solutions  

---

### **Step 1: Defining the Web Application Testing Solution**  
- **Application Context**: The application runs on Kubernetes and interacts with a MongoDB database.  
- **Testing Stack**:  
  - **Functional & API Testing**: `pytest`, `requests`, `pytest-asyncio`, `httpx`, and `pytest-mock`.  
  - **Performance Testing**: `Locust` for load testing.  
  - **CI/CD Integration**: `GitHub Actions` for automated testing workflows.  
  - **Reporting Solutions**: `Allure`, `pytest-html`, `pytest-reportlog`, `Loguru`, or `Junit XML`.  

---

### **Step 2: Implementing API Tests using `pytest`**  

#### **Installation of Required Packages**  
```sh
pip install pytest pytest-asyncio requests httpx pytest-mock pytest-html allure-pytest
```

#### **Project Structure**
```
tests/
│── api/
│   ├── test_users.py
│   ├── test_orders.py
│── performance/
│   ├── locustfile.py
│── conftest.py
│── pytest.ini
.github/
│── workflows/
│   ├── ci-tests.yml
reports/
```

#### **Sample API Test (`test_users.py`)**  
```python
import pytest
import requests

BASE_URL = "http://your-k8s-service/api"

@pytest.fixture
def user_payload():
    return {"username": "testuser", "password": "secure123"}

def test_create_user(user_payload):
    response = requests.post(f"{BASE_URL}/users", json=user_payload)
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

---

### **Step 3: Running Tests in GitHub Actions CI/CD**  

#### **CI/CD Workflow (`ci-tests.yml`)**
```yaml
name: API Testing CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run API Tests
        run: pytest tests/api --html=reports/api_test_report.html --self-contained-html

      - name: Upload Test Report
        uses: actions/upload-artifact@v3
        with:
          name: api-test-report
          path: reports/api_test_report.html
```

---

### **Step 4: Implementing Performance Tests with Locust**  

#### **Installation**
```sh
pip install locust
```

#### **Sample Performance Test (`locustfile.py`)**
```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_users(self):
        self.client.get("/users")

    @task
    def create_user(self):
        self.client.post("/users", json={"username": "testuser", "password": "secure123"})
```

#### **Run Locust Test Locally**
```sh
locust -f tests/performance/locustfile.py --host http://your-k8s-service
```

---

### **Step 5: Performance Test Automation in GitHub Actions**  

#### **CI/CD Workflow for Performance Testing (`ci-performance.yml`)**
```yaml
name: Performance Testing CI/CD

on:
  schedule:
    - cron: "0 3 * * 1" # Runs every Monday at 3 AM

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: pip install locust

      - name: Run Performance Test
        run: |
            locust -f tests/performance/locustfile.py \
              --headless -u 10 -r 1 \
              --csv locust_report \
              --host http://your-k8s-service
  
      - name: Upload Locust Report Artifacts
        uses: actions/upload-artifact@v3
        with:
            name: locust-performance-report
            path: |
              reports/locust_report_stats.csv
              reports/locust_report_failures.csv
              reports/locust_report_distribution.csv
```

---

### **Step 6: Reporting Solutions**

#### **Option 1: `pytest-html`**
- Generates an HTML report for test results.
- Usage:  
```sh
pytest --html=reports/test_report.html --self-contained-html
```

#### **Option 2: `Allure Reports`**
- Install:  
```sh
pip install allure-pytest
```
- Usage:  
```sh
pytest --alluredir=reports/allure
allure serve reports/allure
```

#### **Option 3: `pytest-reportlog`**
- Generates structured JSON reports.
- Usage:  
```sh
pytest --report-log=reports/test_results.json
```

---

### **Step 7: Kubernetes Deployment for Testing**

#### **Sample `k8s` Deployment (`test-app.yaml`)**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-app
  template:
    metadata:
      labels:
        app: test-app
    spec:
      containers:
      - name: test-container
        image: myregistry.com/test-app:latest
        ports:
        - containerPort: 8080
        env:
        - name: MONGO_URI
          value: "mongodb://mongo-service:27017/testdb"
---
apiVersion: v1
kind: Service
metadata:
  name: test-app-service
spec:
  selector:
    app: test-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

---

### **Step 8: Running Tests Against the Kubernetes Cluster**  

#### **Port Forwarding to Access the Application**
```sh
kubectl port-forward service/test-app-service 8080:80
```

#### **Triggering API Tests**
```sh
pytest --base-url http://localhost:8080
```

---

### **Final Deliverables**  
1. **Automated API Tests** with `pytest`  
2. **Performance Testing** with `Locust`  
3. **GitHub Actions CI/CD Pipelines** for test automation  
4. **Multiple Reporting Options**  
5. **Tested Kubernetes Cluster Setup**  

---

### **How to Use the Solution**
1. Clone the repository:  
   ```sh
   git clone https://github.com/your-repo.git && cd your-repo
   ```
2. Run API tests locally:  
   ```sh
   pytest tests/api --html=reports/api_report.html
   ```
3. Run Performance tests locally:  
   ```sh
   locust -f tests/performance/locustfile.py --host http://your-k8s-service
   ```
4. Deploy to Kubernetes and test:  
   ```sh
   kubectl apply -f k8s/test-app.yaml
   ```

---

This setup provides a **scalable, automated** solution for testing APIs and performance in a **Kubernetes environment** with full CI/CD integration and multiple reporting options.



### Elaborate on Locust scaling tests
### **Running a Locust Performance Test at Scale**

Locust allows for distributed load testing where multiple users (virtual clients) simulate requests to an application. You can scale your performance test using various parameters, input data strategies, and execution configurations.

---

### **1. Running Locust at Scale - Key Parameters & Scenarios**
When running Locust, you can control several aspects of the test execution by adjusting parameters:

| Parameter | Description |
|-----------|------------|
| `-f` | Specifies the Locust file to run (e.g., `locustfile.py`). |
| `--headless` | Runs Locust without the UI, useful for CI/CD pipelines. |
| `-u` or `--users` | Number of concurrent virtual users (simulated clients). |
| `-r` or `--spawn-rate` | Number of users to add per second until the target is reached. |
| `--host` | The base URL of the application under test. |
| `--run-time` | Specifies the test duration (e.g., `--run-time 5m` for 5 minutes). |
| `--csv` | Generates CSV output for results analysis. |
| `--html` | Generates an HTML report for the test run. |
| `--logfile` | Stores logs for debugging. |
| `--worker` | Runs Locust in distributed mode with workers. |
| `--master` | Runs Locust in distributed mode as the master. |

#### **Example: Running a Large-Scale Locust Test**
```sh
locust -f tests/performance/locustfile.py --headless -u 1000 -r 50 --host http://your-k8s-service --run-time 10m --csv reports/locust_results
```
This command:
- Spawns **1,000 virtual users** (`-u 1000`).
- Adds **50 new users per second** (`-r 50`).
- Runs the test for **10 minutes** (`--run-time 10m`).
- Targets `http://your-k8s-service`.
- Saves test results in CSV format (`--csv reports/locust_results`).

---

### **2. Explanation of the Example Command**
```sh
locust -f tests/performance/locustfile.py --headless -u 10 -r 1 --host http://your-k8s-service
```
- `-f tests/performance/locustfile.py` → Runs the `locustfile.py` script located in `tests/performance/`.
- `--headless` → Runs Locust in CLI mode without the web UI.
- `-u 10` → Simulates 10 concurrent users.
- `-r 1` → Spawns 1 user per second until 10 users are active.
- `--host http://your-k8s-service` → Sets the target URL of the application.

This setup is **a small-scale test** for local verification before running a larger test in production.

---

### **3. Explanation of `locustfile.py`**
#### **Basic Locust Test**
```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)  # Each user waits 1-3 sec between requests

    @task
    def get_users(self):
        self.client.get("/users")

    @task
    def create_user(self):
        self.client.post("/users", json={"username": "testuser", "password": "secure123"})
```

#### **Breakdown of `locustfile.py`**
1. **`HttpUser`** → Represents a virtual user.
2. **`wait_time = between(1, 3)`** → Each user waits between 1 and 3 seconds before making the next request.
3. **`@task`** → Marks a method as a user action.
4. **`self.client.get("/users")`** → Simulates a GET request to fetch users.
5. **`self.client.post("/users", json={"username": "testuser", "password": "secure123"})`** → Simulates a POST request to create a user.

---

### **4. Scaling Input Data Dynamically**
Static values are not realistic for performance tests. Instead, input data should come from **scalable and robust sources**.

#### **Best Practices for Dynamic Input Data**
1. **Using a CSV File for Large Datasets**
2. **Using a Faker Library for Randomized User Data**
3. **Using a Database Query to Fetch Test Data**

---

#### **Option 1: CSV-Based Data (Best for Large, Predefined User Data)**
If you have a dataset of users, you can load them dynamically.

##### **Example: `users.csv`**
```
username,password
user1,password1
user2,password2
user3,password3
```

##### **Locust File Using CSV**
```python
import csv
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.users = self.load_users_from_csv("users.csv")

    def load_users_from_csv(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)

    @task
    def create_user(self):
        user = self.users.pop()
        self.client.post("/users", json={"username": user["username"], "password": user["password"]})
```

**Pros**:
✔️ Best for large preloaded datasets.  
✔️ Ensures repeatability.  

**Cons**:
❌ Harder to maintain if data needs frequent updates.

---

#### **Option 2: Using Faker Library (Best for Randomized User Data)**
Instead of static data, we can generate **random user details**.

##### **Installation**
```sh
pip install faker
```

##### **Locust File Using Faker**
```python
from locust import HttpUser, task, between
from faker import Faker

fake = Faker()

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_user(self):
        user = {"username": fake.user_name(), "password": fake.password()}
        self.client.post("/users", json=user)
```

**Pros**:
✔️ Great for testing **randomized scenarios**.  
✔️ No need to maintain external datasets.  

**Cons**:
❌ Hard to **track specific user behavior** over time.  
❌ Some APIs may need predictable input.  

---

#### **Option 3: Fetching Data from a Database (Best for Realistic Testing)**
For production-like testing, fetch user credentials directly from **MongoDB**.

##### **Locust File Fetching Data from MongoDB**
```python
from locust import HttpUser, task, between
from pymongo import MongoClient

class APIUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        client = MongoClient("mongodb://your-db-host:27017/")
        db = client["testdb"]
        self.users = list(db.users.find({}, {"_id": 0, "username": 1, "password": 1}))

    @task
    def create_user(self):
        if self.users:
            user = self.users.pop()
            self.client.post("/users", json={"username": user["username"], "password": user["password"]})
```

**Pros**:
✔️ Matches real-world production conditions.  
✔️ Uses **actual** database records.  

**Cons**:
❌ Requires **database access**.  
❌ Can slow down test execution if queries are inefficient.  

---

### **Final Thoughts: Choosing the Best Input Method**
| Method | Best For | Pros | Cons |
|--------|---------|------|------|
| **CSV-Based** | Large datasets | Repeatability, easy to debug | Hard to maintain |
| **Faker** | Randomized test data | No dataset needed | Cannot track specific users |
| **Database Query** | Production-like scenarios | Uses real data | Requires DB access |

For **scalability**, using **CSV** or **MongoDB** is best. For **randomization**, `Faker` is preferred.

---

### **Next Steps**
- Run a large-scale test:
```sh
locust -f tests/performance/locustfile.py --headless -u 1000 -r 50 --host http://your-k8s-service --run-time 15m --csv reports/locust_results
```
- Use different user datasets (`CSV`, `Faker`, or `MongoDB`).
- Integrate Locust into CI/CD for automated performance testing.

This approach ensures **scalable, realistic performance testing** for web applications running on Kubernetes. 🚀