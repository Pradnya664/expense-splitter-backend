from fastapi import APIRouter, HTTPException
from models import Expense
from database import expenses_collection
from bson import ObjectId
from collections import defaultdict
#from pymongo.errors import InvalidId

router = APIRouter()

@router.post("/expenses")
def add_expense(expense: Expense):
    expense_dict = expense.dict()
    if expense.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    
    if not expense.description.strip():
        raise HTTPException(status_code=400, detail="Description cannot be empty")
    
    if not expense.paid_by.strip():
        raise HTTPException(status_code=400, detail="Paid by cannot be empty")

    # Strip timezone info if present (Mongo doesn't like timezone-aware datetime)
    if expense_dict.get("timestamp") and expense_dict["timestamp"].tzinfo:
        expense_dict["timestamp"] = expense_dict["timestamp"].replace(tzinfo=None)

    result = expenses_collection.insert_one(expense_dict)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to add expense")

    expense_dict["_id"] = str(result.inserted_id)

    return {
        "success": True,
        "data": expense_dict,
        "message": "Expense added successfully"
    }

@router.get("/expenses")
def get_all_expenses():
    expenses = []

    for expense in expenses_collection.find():
        expense["_id"] = str(expense["_id"])  # Convert ObjectId to string
        expenses.append(expense)

    return {
        "success": True,
        "data": expenses,
        "message": f"{len(expenses)} expense(s) found"
    }

@router.put("/expenses/{expense_id}")
def update_expense(expense_id: str, updated_expense: Expense):
    try:
        _id = ObjectId(expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense ID format")

    updated_data = updated_expense.dict()
    result = expenses_collection.update_one({"_id": _id}, {"$set": updated_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {
        "success": True,
        "message": "Expense updated successfully"
    }

@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str):
    try:
        _id = ObjectId(expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense ID format")

    result = expenses_collection.delete_one({"_id": _id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {
        "success": True,
        "message": "Expense deleted successfully"
    }

@router.get("/people")
def get_people():
    people_set = set()
    for expense in expenses_collection.find():
        people_set.add(expense["paid_by"])

    return {
        "success": True,
        "data": list(people_set),
        "message": f"{len(people_set)} person(s) found"
    }



@router.get("/balances")
def get_balances():
    people = set()
    total_spent = 0
    spent_by = defaultdict(float)

    expenses = list(expenses_collection.find())
    for expense in expenses:
        payer = expense["paid_by"]
        amount = float(expense["amount"])
        total_spent += amount
        spent_by[payer] += amount
        people.add(payer)

    if not people:
        return {"success": True, "data": {}, "message": "No expenses found"}

    fair_share = total_spent / len(people)
    balances = {person: round(spent_by[person] - fair_share, 2) for person in people}

    return {
        "success": True,
        "data": balances,
        "message": "Net balances for each person"
    }

@router.get("/settlements")
def get_settlements():
    balances = get_balances()["data"]

    # Separate creditors and debtors
    creditors = []
    debtors = []

    for person, balance in balances.items():
        if balance > 0:
            creditors.append((person, balance))
        elif balance < 0:
            debtors.append((person, -balance))  # negate for ease

    creditors.sort(key=lambda x: -x[1])  # highest credit first
    debtors.sort(key=lambda x: -x[1])    # highest debt first

    settlements = []

    i = j = 0
    while i < len(debtors) and j < len(creditors):
        debtor, debt_amt = debtors[i]
        creditor, credit_amt = creditors[j]

        amount = min(debt_amt, credit_amt)
        settlements.append({
            "from": debtor,
            "to": creditor,
            "amount": round(amount, 2)
        })

        debtors[i] = (debtor, debt_amt - amount)
        creditors[j] = (creditor, credit_amt - amount)

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return {
        "success": True,
        "data": settlements,
        "message": "Simplified settlement transactions"
    }

