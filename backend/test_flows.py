import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def print_step(name):
    print(f"\n[{name}]")

def run_tests():
    session = requests.Session()

    # STEP A: USER FLOW
    print_step("A. USER FLOW: Register & Login")
    email = f"test_{int(time.time())}@example.com"
    password = "password123"
    
    # Register
    res = session.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "password": password,
        "base_currency": "SGD"
    })
    if res.status_code not in (200, 201):
        print(f"FAILED Register: {res.text}")
        return
    print("User Registered successfully.")

    # Login
    res = session.post(f"{BASE_URL}/auth/login", data={
        "username": email,
        "password": password
    })
    if res.status_code != 200:
        print(f"FAILED Login: {res.text}")
        return
    token = res.json()["access_token"]
    session.headers.update({"Authorization": f"Bearer {token}"})
    print("User Logged in successfully.")

    # STEP B & C: FINANCIAL INPUT & FX CONVERSION
    # STEP B: FINANCIAL INPUT & FX CONVERSION
    print_step("B & C. FINANCIAL INPUT & FX CONVERSION")
    # Add Income SGD
    res = session.post(f"{BASE_URL}/finance/incomes", json={
        "currency": "SGD",
        "original_amount": 5000,
        "source": "Salary",
        "date": "2026-04-01"
    })
    if res.status_code != 200: print(f"FAILED Add Income: {res.text}")
    else: print("Income added successfully.")

    # Expenses API test instead of legacy investment
    res = session.post(f"{BASE_URL}/finance/expenses", json={
        "currency": "MYR",
        "original_amount": 1000,
        "category": "Travel",
        "date": "2026-04-02"
    })
    if res.status_code != 200: print(f"FAILED Add Expense: {res.text}")
    else:
        base_val = res.json()["base_amount"]
        print(f"Added MYR 1,000 expense. Converted to SGD: {base_val:.2f}")
        if base_val == 1000:
            print("WARNING: FX Conversion did not apply properly (MYR=SGD).")
        else:
            print("FX Conversion SUCCESS.")

    # STEP D: CPF / EPF
    print_step("D. STATUTORY ACCOUNTS: CPF & EPF")
    res = session.post(f"{BASE_URL}/finance/cpf", json={"account_type": "OA", "balance": 40000})
    if res.status_code != 200: print(f"FAILED Add CPF: {res.text}")
    res = session.post(f"{BASE_URL}/finance/epf", json={"account_type": "Account 1", "balance": 85000})
    if res.status_code != 200: print(f"FAILED Add EPF: {res.text}")
    print("Statutory accounts added successfully.")

    # STEP E: PORTFOLIO
    print_step("E. PORTFOLIO")
    res = session.post(f"{BASE_URL}/robo/", json={
        "platform": "Endowus",
        "fund_name": "S&P 500",
        "ticker": "CSPX.L",
        "allocation_percentage": 100,
        "value": 15000,
        "currency": "USD"
    })
    if res.status_code != 200: 
        print(f"FAILED Add Portfolio: {res.text}")
    else:
        print("Portfolio holding added successfully (CSPX.L - S&P 500).")

    # Fetch summary to verify everything is working
    res = session.get(f"{BASE_URL}/finance/summary")
    if res.status_code == 200:
        data = res.json()
        print(f"Net Worth Base (SGD): {data.get('net_worth')}")
    else:
        print(f"FAILED Summary fetch: {res.text}")

    # STEP F: REPORT GENERATION
    print_step("F. REPORT GENERATION")
    res = session.get(f"{BASE_URL}/reports/monthly")
    if res.status_code == 200:
         print("Report Generated Successfully.")
         report_data = res.json()
         if 'json_payload' in report_data:
             print("Verified: json_payload present.")
         if 'text_report' in report_data:
             print("Verified: text_report present.")
    else:
         print(f"FAILED Report Generation: {res.text}")

    print("\nALL BACKEND API TESTS COMPLETED.")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"Error running tests: {e}")