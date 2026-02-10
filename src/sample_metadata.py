"""
Generate sample Oracle metadata for testing without a real Oracle database.
This creates a realistic schema structure for an HR system.
"""

import json
import os

def generate_sample_metadata():
    """Generate sample Oracle metadata structure"""
    
    metadata = {
        "tables": [
            {
                "table_name": "EMPLOYEES",
                "owner": "HR",
                "tablespace_name": "USERS",
                "num_rows": 107,
                "columns": [
                    {"column_name": "EMPLOYEE_ID", "data_type": "NUMBER", "nullable": "N", "data_length": 22},
                    {"column_name": "FIRST_NAME", "data_type": "VARCHAR2", "nullable": "Y", "data_length": 20},
                    {"column_name": "LAST_NAME", "data_type": "VARCHAR2", "nullable": "N", "data_length": 25},
                    {"column_name": "EMAIL", "data_type": "VARCHAR2", "nullable": "N", "data_length": 25},
                    {"column_name": "PHONE_NUMBER", "data_type": "VARCHAR2", "nullable": "Y", "data_length": 20},
                    {"column_name": "HIRE_DATE", "data_type": "DATE", "nullable": "N", "data_length": 7},
                    {"column_name": "JOB_ID", "data_type": "VARCHAR2", "nullable": "N", "data_length": 10},
                    {"column_name": "SALARY", "data_type": "NUMBER", "nullable": "Y", "data_length": 22},
                    {"column_name": "COMMISSION_PCT", "data_type": "NUMBER", "nullable": "Y", "data_length": 22},
                    {"column_name": "MANAGER_ID", "data_type": "NUMBER", "nullable": "Y", "data_length": 22},
                    {"column_name": "DEPARTMENT_ID", "data_type": "NUMBER", "nullable": "Y", "data_length": 22}
                ],
                "indexes": [
                    {"index_name": "EMP_PK", "index_type": "NORMAL", "uniqueness": "UNIQUE", "columns": ["EMPLOYEE_ID"]},
                    {"index_name": "EMP_EMAIL_UK", "index_type": "NORMAL", "uniqueness": "UNIQUE", "columns": ["EMAIL"]},
                    {"index_name": "EMP_DEPT_FK_IDX", "index_type": "NORMAL", "uniqueness": "NONUNIQUE", "columns": ["DEPARTMENT_ID"]},
                    {"index_name": "EMP_JOB_FK_IDX", "index_type": "NORMAL", "uniqueness": "NONUNIQUE", "columns": ["JOB_ID"]},
                    {"index_name": "EMP_MANAGER_FK_IDX", "index_type": "NORMAL", "uniqueness": "NONUNIQUE", "columns": ["MANAGER_ID"]}
                ],
                "constraints": [
                    {"constraint_name": "EMP_PK", "constraint_type": "P", "columns": ["EMPLOYEE_ID"]},
                    {"constraint_name": "EMP_EMAIL_UK", "constraint_type": "U", "columns": ["EMAIL"]},
                    {"constraint_name": "EMP_DEPT_FK", "constraint_type": "R", "columns": ["DEPARTMENT_ID"], "r_table": "DEPARTMENTS"},
                    {"constraint_name": "EMP_JOB_FK", "constraint_type": "R", "columns": ["JOB_ID"], "r_table": "JOBS"},
                    {"constraint_name": "EMP_MANAGER_FK", "constraint_type": "R", "columns": ["MANAGER_ID"], "r_table": "EMPLOYEES"}
                ]
            },
            {
                "table_name": "DEPARTMENTS",
                "owner": "HR",
                "tablespace_name": "USERS",
                "num_rows": 27,
                "columns": [
                    {"column_name": "DEPARTMENT_ID", "data_type": "NUMBER", "nullable": "N", "data_length": 22},
                    {"column_name": "DEPARTMENT_NAME", "data_type": "VARCHAR2", "nullable": "N", "data_length": 30},
                    {"column_name": "MANAGER_ID", "data_type": "NUMBER", "nullable": "Y", "data_length": 22},
                    {"column_name": "LOCATION_ID", "data_type": "NUMBER", "nullable": "Y", "data_length": 22}
                ],
                "indexes": [
                    {"index_name": "DEPT_PK", "index_type": "NORMAL", "uniqueness": "UNIQUE", "columns": ["DEPARTMENT_ID"]},
                    {"index_name": "DEPT_LOC_FK_IDX", "index_type": "NORMAL", "uniqueness": "NONUNIQUE", "columns": ["LOCATION_ID"]}
                ],
                "constraints": [
                    {"constraint_name": "DEPT_PK", "constraint_type": "P", "columns": ["DEPARTMENT_ID"]},
                    {"constraint_name": "DEPT_LOC_FK", "constraint_type": "R", "columns": ["LOCATION_ID"], "r_table": "LOCATIONS"}
                ]
            },
            {
                "table_name": "JOBS",
                "owner": "HR",
                "tablespace_name": "USERS",
                "num_rows": 19,
                "columns": [
                    {"column_name": "JOB_ID", "data_type": "VARCHAR2", "nullable": "N", "data_length": 10},
                    {"column_name": "JOB_TITLE", "data_type": "VARCHAR2", "nullable": "N", "data_length": 35},
                    {"column_name": "MIN_SALARY", "data_type": "NUMBER", "nullable": "Y", "data_length": 22},
                    {"column_name": "MAX_SALARY", "data_type": "NUMBER", "nullable": "Y", "data_length": 22}
                ],
                "indexes": [
                    {"index_name": "JOB_PK", "index_type": "NORMAL", "uniqueness": "UNIQUE", "columns": ["JOB_ID"]}
                ],
                "constraints": [
                    {"constraint_name": "JOB_PK", "constraint_type": "P", "columns": ["JOB_ID"]}
                ]
            },
            {
                "table_name": "LOCATIONS",
                "owner": "HR",
                "tablespace_name": "USERS",
                "num_rows": 23,
                "columns": [
                    {"column_name": "LOCATION_ID", "data_type": "NUMBER", "nullable": "N", "data_length": 22},
                    {"column_name": "STREET_ADDRESS", "data_type": "VARCHAR2", "nullable": "Y", "data_length": 40},
                    {"column_name": "POSTAL_CODE", "data_type": "VARCHAR2", "nullable": "Y", "data_length": 12},
                    {"column_name": "CITY", "data_type": "VARCHAR2", "nullable": "N", "data_length": 30},
                    {"column_name": "STATE_PROVINCE", "data_type": "VARCHAR2", "nullable": "Y", "data_length": 25},
                    {"column_name": "COUNTRY_ID", "data_type": "CHAR", "nullable": "Y", "data_length": 2}
                ],
                "indexes": [
                    {"index_name": "LOC_PK", "index_type": "NORMAL", "uniqueness": "UNIQUE", "columns": ["LOCATION_ID"]},
                    {"index_name": "LOC_COUNTRY_FK_IDX", "index_type": "NORMAL", "uniqueness": "NONUNIQUE", "columns": ["COUNTRY_ID"]}
                ],
                "constraints": [
                    {"constraint_name": "LOC_PK", "constraint_type": "P", "columns": ["LOCATION_ID"]},
                    {"constraint_name": "LOC_COUNTRY_FK", "constraint_type": "R", "columns": ["COUNTRY_ID"], "r_table": "COUNTRIES"}
                ]
            },
            {
                "table_name": "COUNTRIES",
                "owner": "HR",
                "tablespace_name": "USERS",
                "num_rows": 25,
                "columns": [
                    {"column_name": "COUNTRY_ID", "data_type": "CHAR", "nullable": "N", "data_length": 2},
                    {"column_name": "COUNTRY_NAME", "data_type": "VARCHAR2", "nullable": "Y", "data_length": 40},
                    {"column_name": "REGION_ID", "data_type": "NUMBER", "nullable": "Y", "data_length": 22}
                ],
                "indexes": [
                    {"index_name": "COUNTRY_PK", "index_type": "NORMAL", "uniqueness": "UNIQUE", "columns": ["COUNTRY_ID"]}
                ],
                "constraints": [
                    {"constraint_name": "COUNTRY_PK", "constraint_type": "P", "columns": ["COUNTRY_ID"]},
                    {"constraint_name": "COUNTRY_REG_FK", "constraint_type": "R", "columns": ["REGION_ID"], "r_table": "REGIONS"}
                ]
            },
            {
                "table_name": "REGIONS",
                "owner": "HR",
                "tablespace_name": "USERS",
                "num_rows": 4,
                "columns": [
                    {"column_name": "REGION_ID", "data_type": "NUMBER", "nullable": "N", "data_length": 22},
                    {"column_name": "REGION_NAME", "data_type": "VARCHAR2", "nullable": "Y", "data_length": 25}
                ],
                "indexes": [
                    {"index_name": "REG_PK", "index_type": "NORMAL", "uniqueness": "UNIQUE", "columns": ["REGION_ID"]}
                ],
                "constraints": [
                    {"constraint_name": "REG_PK", "constraint_type": "P", "columns": ["REGION_ID"]}
                ]
            }
        ]
    }
    
    return metadata


def save_metadata(metadata, filename="oracle_metadata.json"):
    """Save metadata to JSON file"""
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)
    
    with open(filepath, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Sample metadata saved to {filepath}")
    print(f"✓ Generated {len(metadata['tables'])} tables")
    
    total_columns = sum(len(table['columns']) for table in metadata['tables'])
    total_indexes = sum(len(table['indexes']) for table in metadata['tables'])
    total_constraints = sum(len(table['constraints']) for table in metadata['tables'])
    
    print(f"✓ Total columns: {total_columns}")
    print(f"✓ Total indexes: {total_indexes}")
    print(f"✓ Total constraints: {total_constraints}")
    
    return filepath


if __name__ == "__main__":
    print("Generating sample Oracle metadata...")
    metadata = generate_sample_metadata()
    save_metadata(metadata)
    print("\nReady to build knowledge graph! Run: python src/build_graph.py")
