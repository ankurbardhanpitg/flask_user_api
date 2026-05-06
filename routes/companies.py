from datetime import datetime
import json
from pathlib import Path

from flask import Blueprint, jsonify, request
from middleware.authentication import token_required

companies_bp = Blueprint("companies", __name__)

DATA_FILE = Path(__file__).resolve().parent.parent / "companies.json"


def read_companies():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        try:
            content = f.read().strip()
            return json.loads(content) if content else []
        except json.JSONDecodeError:
            return []


def write_companies(companies):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(companies, f, indent=4)


def next_company_id(companies):
    numeric_ids = []
    for company in companies:
        company_id = company.get("id")
        if isinstance(company_id, (int, float)):
            numeric_ids.append(int(company_id))
    return (max(numeric_ids) + 1) if numeric_ids else int(datetime.now().timestamp() * 1000)


# POST /companies - Create a new company (requires name and email).
@companies_bp.route("/companies", methods=["POST"])
@token_required
def add_company():
    data = request.json or {}
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"message": "name and email are required"}), 400

    companies = read_companies()

    new_company = {
        "id": next_company_id(companies),
        "name": name,
        "email": email,
    }

    companies.append(new_company)
    write_companies(companies)

    return jsonify(new_company), 201
# End of POST /companies - Create a new company (requires name and email).

# GET /companies - Return all companies.
@companies_bp.route("/companies", methods=["GET"])
@token_required
def get_companies():
    companies = read_companies()
    return jsonify(companies)

# End of GET /companies - Return all companies.

# PUT /companies/<company_id> - Update an existing company by ID.
@companies_bp.route("/companies/<int:company_id>", methods=["PUT"])
@token_required
def update_company(company_id):
    data = request.json or {}
    companies = read_companies()

    for company in companies:
        if company["id"] == company_id:
            company["name"] = data.get("name", company["name"])
            company["email"] = data.get("email", company["email"])
            write_companies(companies)
            return jsonify(company)

    return jsonify({"message": "Company not found"}), 404
# End of PUT /companies/<company_id> - Update an existing company by ID.

# DELETE /companies/<company_id> - Delete a company by ID.
@companies_bp.route("/companies/<int:company_id>", methods=["DELETE"])
@token_required
def delete_company(company_id):
    companies = read_companies()
    updated_companies = [c for c in companies if c["id"] != company_id]

    if len(companies) == len(updated_companies):
        return jsonify({"message": "Company not found"}), 404

    write_companies(updated_companies)
    return jsonify({"message": "Company deleted"})
# End of DELETE /companies/<company_id> - Delete a company by ID.
