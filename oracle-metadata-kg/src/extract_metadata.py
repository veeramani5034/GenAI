"""
Extract metadata from Oracle database.
Queries system tables to get information about tables, columns, indexes, and constraints.
"""

import oracledb
import json
import os
from dotenv import load_dotenv

load_dotenv()


def connect_to_oracle():
    """Establish connection to Oracle database"""
    try:
        connection = oracledb.connect(
            user=os.getenv('ORACLE_USER'),
            password=os.getenv('ORACLE_PASSWORD'),
            host=os.getenv('ORACLE_HOST'),
            port=int(os.getenv('ORACLE_PORT', 1521)),
            service_name=os.getenv('ORACLE_SERVICE_NAME')
        )
        print("✓ Connected to Oracle database")
        return connection
    except Exception as e:
        print(f"✗ Error connecting to Oracle: {e}")
        raise


def extract_tables(connection, owner=None):
    """Extract table metadata"""
    cursor = connection.cursor()
    
    query = """
        SELECT 
            owner,
            table_name,
            tablespace_name,
            num_rows
        FROM all_tables
        WHERE owner = NVL(:owner, USER)
        ORDER BY table_name
    """
    
    cursor.execute(query, [owner])
    tables = []
    
    for row in cursor:
        tables.append({
            "owner": row[0],
            "table_name": row[1],
            "tablespace_name": row[2],
            "num_rows": row[3]
        })
    
    cursor.close()
    print(f"✓ Extracted {len(tables)} tables")
    return tables


def extract_columns(connection, owner, table_name):
    """Extract column metadata for a table"""
    cursor = connection.cursor()
    
    query = """
        SELECT 
            column_name,
            data_type,
            nullable,
            data_length,
            data_precision,
            data_scale
        FROM all_tab_columns
        WHERE owner = :owner
        AND table_name = :table_name
        ORDER BY column_id
    """
    
    cursor.execute(query, [owner, table_name])
    columns = []
    
    for row in cursor:
        columns.append({
            "column_name": row[0],
            "data_type": row[1],
            "nullable": row[2],
            "data_length": row[3],
            "data_precision": row[4],
            "data_scale": row[5]
        })
    
    cursor.close()
    return columns


def extract_indexes(connection, owner, table_name):
    """Extract index metadata for a table"""
    cursor = connection.cursor()
    
    query = """
        SELECT DISTINCT
            i.index_name,
            i.index_type,
            i.uniqueness
        FROM all_indexes i
        WHERE i.owner = :owner
        AND i.table_name = :table_name
        ORDER BY i.index_name
    """
    
    cursor.execute(query, [owner, table_name])
    indexes = []
    
    for row in cursor:
        index_name = row[0]
        
        # Get columns for this index
        col_cursor = connection.cursor()
        col_query = """
            SELECT column_name
            FROM all_ind_columns
            WHERE index_owner = :owner
            AND index_name = :index_name
            ORDER BY column_position
        """
        col_cursor.execute(col_query, [owner, index_name])
        columns = [col[0] for col in col_cursor]
        col_cursor.close()
        
        indexes.append({
            "index_name": index_name,
            "index_type": row[1],
            "uniqueness": row[2],
            "columns": columns
        })
    
    cursor.close()
    return indexes


def extract_constraints(connection, owner, table_name):
    """Extract constraint metadata for a table"""
    cursor = connection.cursor()
    
    query = """
        SELECT 
            c.constraint_name,
            c.constraint_type,
            c.r_constraint_name
        FROM all_constraints c
        WHERE c.owner = :owner
        AND c.table_name = :table_name
        AND c.constraint_type IN ('P', 'U', 'R', 'C')
        ORDER BY c.constraint_name
    """
    
    cursor.execute(query, [owner, table_name])
    constraints = []
    
    for row in cursor:
        constraint_name = row[0]
        constraint_type = row[1]
        r_constraint_name = row[2]
        
        # Get columns for this constraint
        col_cursor = connection.cursor()
        col_query = """
            SELECT column_name
            FROM all_cons_columns
            WHERE owner = :owner
            AND constraint_name = :constraint_name
            ORDER BY position
        """
        col_cursor.execute(col_query, [owner, constraint_name])
        columns = [col[0] for col in col_cursor]
        col_cursor.close()
        
        constraint_data = {
            "constraint_name": constraint_name,
            "constraint_type": constraint_type,
            "columns": columns
        }
        
        # If foreign key, get referenced table
        if constraint_type == 'R' and r_constraint_name:
            ref_cursor = connection.cursor()
            ref_query = """
                SELECT table_name
                FROM all_constraints
                WHERE owner = :owner
                AND constraint_name = :constraint_name
            """
            ref_cursor.execute(ref_query, [owner, r_constraint_name])
            ref_row = ref_cursor.fetchone()
            if ref_row:
                constraint_data["r_table"] = ref_row[0]
            ref_cursor.close()
        
        constraints.append(constraint_data)
    
    cursor.close()
    return constraints


def extract_all_metadata(owner=None):
    """Extract all metadata from Oracle database"""
    connection = connect_to_oracle()
    
    try:
        # Get tables
        tables = extract_tables(connection, owner)
        
        # For each table, get columns, indexes, and constraints
        for table in tables:
            print(f"Processing {table['table_name']}...")
            table['columns'] = extract_columns(connection, table['owner'], table['table_name'])
            table['indexes'] = extract_indexes(connection, table['owner'], table['table_name'])
            table['constraints'] = extract_constraints(connection, table['owner'], table['table_name'])
        
        metadata = {"tables": tables}
        
        # Save to file
        os.makedirs("data", exist_ok=True)
        filepath = os.path.join("data", "oracle_metadata.json")
        
        with open(filepath, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n✓ Metadata extracted successfully to {filepath}")
        
        total_columns = sum(len(table['columns']) for table in tables)
        total_indexes = sum(len(table['indexes']) for table in tables)
        total_constraints = sum(len(table['constraints']) for table in tables)
        
        print(f"✓ Total tables: {len(tables)}")
        print(f"✓ Total columns: {total_columns}")
        print(f"✓ Total indexes: {total_indexes}")
        print(f"✓ Total constraints: {total_constraints}")
        
        return metadata
        
    finally:
        connection.close()
        print("✓ Database connection closed")


if __name__ == "__main__":
    print("Extracting Oracle metadata...")
    owner = os.getenv('ORACLE_USER')  # Or specify a different schema owner
    extract_all_metadata(owner)
    print("\nReady to build knowledge graph! Run: python src/build_graph.py")
