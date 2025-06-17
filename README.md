# Expense Splitter Backend API

This is a backend API built to help groups of people split expenses fairly and calculate who owes how much to whom. It supports adding shared expenses (like restaurant bills, travel costs, utilities, etc.), automatically calculates balances, and simplifies settlements with minimal transactions.

---

##Tech Stack

This project uses the following technologies:

- **Python**: Core programming language for the backend logic.
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs in Python.
- **Uvicorn**: ASGI server used to run FastAPI applications.
- **In-Memory Python Storage**: For simplicity, expenses and people are stored in-memory using Python data structures (`lists` and `dicts`) instead of a database.
- **Render**: Cloud platform used to deploy the FastAPI app for public access.
- **Postman**: Tool used for API testing. A public Postman collection is provided to demonstrate functionality with realistic data.

---

## Business Logic – How Expense Splitting Works

When an expense is added, the system:

1. **Stores the expense** with amount, description, and the person who paid it.
2. **Adds new people automatically** if they appear in expenses but weren't added manually.
3. **Assumes equal split** of the total amount across all involved people.
4. **Calculates the fair share** each person should have paid.
5. **Compares the amount each person paid** with what they were supposed to pay (fair share).
6. **Generates balances**, showing how much each person owes (negative balance) or is owed (positive balance).
7. **Simplifies the debt**: It tries to reduce the number of transactions required by calculating who should pay whom directly, without intermediaries.

---

##Example of Settlement Calculation

Imagine three friends: Shantanu, Sanket, and Om.

- Total expenses added:
  - Shantanu paid ₹1100
  - Sanket paid ₹450
  - Om paid ₹350
  - Total = ₹1900

- Equal share = ₹1900 / 3 = ₹633.33

- Individual balances:
  - Shantanu: Paid ₹1100 → Is owed ₹466.67
  - Sanket: Paid ₹450 → Owes ₹183.33
  - Om: Paid ₹350 → Owes ₹283.33

- Optimized settlement (who pays whom):
  - Sanket pays ₹183.33 to Shantanu
  - Om pays ₹283.33 to Shantanu

This way, everyone’s balance becomes zero, and the system minimizes the number of money transfers.

---

## API Overview

The API provides the following endpoints:

- `/expenses` (GET): View all expenses
- `/expenses` (POST): Add a new expense
- `/expenses/{id}` (PUT): Update an existing expense
- `/expenses/{id}` (DELETE): Remove an expense
- `/people` (GET): View all unique people derived from expenses
- `/balances` (GET): See how much each person owes or is owed
- `/settlements` (GET): See simplified "who pays whom" results

---

## Testing the API

A public Postman collection is available and includes:

- Add expense examples
- Update and delete operations
- Settlement and balances
- Edge case scenarios like invalid input and missing data

Public collection link (Gist):  
https://gist.github.com/Pradnya664/6826558e4624731cb6338032008df67d

To test:
1. Open the link above
2. Click "Raw" to copy the raw JSON
3. Open Postman → Import → Paste Raw Text → Done!

---

## Deployment

The application is hosted publicly on Render.  
To deploy your own version:

1. Push your FastAPI code to GitHub
2. Sign up for a free Render.com account
3. Create a new Web Service from your repo
4. Use `uvicorn main:app --host=0.0.0.0 --port=10000` as your start command

Your API will be available at `https://<your-app-name>.onrender.com`

---

## Known Limitations

- Only equal expense splitting is supported currently
- Data is stored in memory; not persistent across restarts
- No authentication or user roles implemented
- Names are case-sensitive (e.g., “Om” ≠ “om”)
- 
---

This project is inspired by apps like Splitwise and designed to demonstrate backend design, REST APIs, and real-world logic handling.
