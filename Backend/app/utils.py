# backend/app/utils.py

# Correct mappings based on LabelEncoder alphabetical encoding

SEX_MAP = {
    "F": 0,
    "M": 1
}

BP_MAP = {
    "HIGH": 0,
    "LOW": 1,
    "NORMAL": 2
}

CHOL_MAP = {
    "HIGH": 0,
    "NORMAL": 1
}

# Drug label decoding (from label encoder training)
DRUG_MAP = {
    0: "DrugA",
    1: "DrugB",
    2: "DrugC",
    3: "DrugX",
    4: "DrugY"
}
