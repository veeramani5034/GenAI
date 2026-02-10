"""
Build Neo4j knowledge graph from Oracle metadata.
Creates nodes for tables, columns, indexes, and relationships between them.
"""

import json
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


class Neo4jGraphBuilder:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        print("✓ Connected to Neo4j")
    
    def close(self):
        self.driver.close()
        print("✓ Neo4j connection closed")
    
    def clear_database(self):
        """Clear all nodes and relationships"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print("✓ Database cleared")
    
    def create_table_node(self, table_data):
        """Create a Table node"""
        with self.driver.session() as session:
            query = """
            CREATE (t:Table {
                name: $name,
                owner: $owner,
                tablespace: $tablespace,
                num_rows: $num_rows
            })
            """
            session.run(query, 
                name=table_data['table_name'],
                owner=table_data['owner'],
                tablespace=table_data.get('tablespace_name'),
                num_rows=table_data.get('num_rows', 0)
            )
    
    def create_column_nodes(self, table_name, columns):
        """Create Column nodes and relationships to table"""
        with self.driver.session() as session:
            for idx, col in enumerate(columns):
                query = """
                MATCH (t:Table {name: $table_name})
                CREATE (c:Column {
                    name: $col_name,
                    data_type: $data_type,
                    nullable: $nullable,
                    data_length: $data_length,
                    position: $position
                })
                CREATE (t)-[:HAS_COLUMN]->(c)
                """
                session.run(query,
                    table_name=table_name,
                    col_name=col['column_name'],
                    data_type=col['data_type'],
                    nullable=col['nullable'],
                    data_length=col.get('data_length'),
                    position=idx + 1
                )
    
    def create_index_nodes(self, table_name, indexes):
        """Create Index nodes and relationships"""
        with self.driver.session() as session:
            for idx in indexes:
                query = """
                MATCH (t:Table {name: $table_name})
                CREATE (i:Index {
                    name: $index_name,
                    type: $index_type,
                    uniqueness: $uniqueness,
                    columns: $columns
                })
                CREATE (t)-[:HAS_INDEX]->(i)
                """
                session.run(query,
                    table_name=table_name,
                    index_name=idx['index_name'],
                    index_type=idx['index_type'],
                    uniqueness=idx['uniqueness'],
                    columns=idx['columns']
                )
                
                # Link index to columns
                for col_name in idx['columns']:
                    col_query = """
                    MATCH (i:Index {name: $index_name})
                    MATCH (t:Table {name: $table_name})-[:HAS_COLUMN]->(c:Column {name: $col_name})
                    CREATE (i)-[:INDEXES_COLUMN]->(c)
                    """
                    session.run(col_query,
                        index_name=idx['index_name'],
                        col_name=col_name,
                        table_name=table_name
                    )
    
    def create_constraint_nodes(self, table_name, constraints):
        """Create Constraint nodes and relationships"""
        with self.driver.session() as session:
            for cons in constraints:
                constraint_type_map = {
                    'P': 'PRIMARY_KEY',
                    'U': 'UNIQUE',
                    'R': 'FOREIGN_KEY',
                    'C': 'CHECK'
                }
                
                query = """
                MATCH (t:Table {name: $table_name})
                CREATE (con:Constraint {
                    name: $constraint_name,
                    type: $constraint_type,
                    columns: $columns
                })
                CREATE (t)-[:HAS_CONSTRAINT]->(con)
                """
                session.run(query,
                    table_name=table_name,
                    constraint_name=cons['constraint_name'],
                    constraint_type=constraint_type_map.get(cons['constraint_type'], 'UNKNOWN'),
                    columns=cons['columns']
                )
                
                # If foreign key, create relationship to referenced table
                if cons['constraint_type'] == 'R' and 'r_table' in cons:
                    fk_query = """
                    MATCH (t1:Table {name: $table_name})
                    MATCH (t2:Table {name: $ref_table})
                    CREATE (t1)-[:HAS_FOREIGN_KEY {
                        constraint_name: $constraint_name,
                        columns: $columns
                    }]->(t2)
                    """
                    session.run(fk_query,
                        table_name=table_name,
                        ref_table=cons['r_table'],
                        constraint_name=cons['constraint_name'],
                        columns=cons['columns']
                    )
    
    def create_indexes_for_performance(self):
        """Create Neo4j indexes for better query performance"""
        with self.driver.session() as session:
            indexes = [
                "CREATE INDEX table_name_idx IF NOT EXISTS FOR (t:Table) ON (t.name)",
                "CREATE INDEX column_name_idx IF NOT EXISTS FOR (c:Column) ON (c.name)",
                "CREATE INDEX index_name_idx IF NOT EXISTS FOR (i:Index) ON (i.name)",
                "CREATE INDEX constraint_name_idx IF NOT EXISTS FOR (con:Constraint) ON (con.name)"
            ]
            
            for idx_query in indexes:
                session.run(idx_query)
        
        print("✓ Created Neo4j indexes for performance")
    
    def build_graph(self, metadata):
        """Build the complete knowledge graph"""
        print("\nBuilding knowledge graph...")
        
        # Clear existing data
        self.clear_database()
        
        tables = metadata['tables']
        total_tables = len(tables)
        
        # Create table nodes
        print(f"\nCreating {total_tables} table nodes...")
        for table in tables:
            self.create_table_node(table)
        print(f"✓ Created {total_tables} table nodes")
        
        # Create columns, indexes, and constraints
        for idx, table in enumerate(tables, 1):
            table_name = table['table_name']
            print(f"[{idx}/{total_tables}] Processing {table_name}...")
            
            if 'columns' in table:
                self.create_column_nodes(table_name, table['columns'])
            
            if 'indexes' in table:
                self.create_index_nodes(table_name, table['indexes'])
            
            if 'constraints' in table:
                self.create_constraint_nodes(table_name, table['constraints'])
        
        # Create performance indexes
        self.create_indexes_for_performance()
        
        print("\n✓ Knowledge graph built successfully!")
        self.print_statistics()
    
    def print_statistics(self):
        """Print graph statistics"""
        with self.driver.session() as session:
            stats = {
                "Tables": session.run("MATCH (t:Table) RETURN count(t) as count").single()['count'],
                "Columns": session.run("MATCH (c:Column) RETURN count(c) as count").single()['count'],
                "Indexes": session.run("MATCH (i:Index) RETURN count(i) as count").single()['count'],
                "Constraints": session.run("MATCH (con:Constraint) RETURN count(con) as count").single()['count'],
                "Foreign Keys": session.run("MATCH ()-[r:HAS_FOREIGN_KEY]->() RETURN count(r) as count").single()['count']
            }
            
            print("\nGraph Statistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")


def load_metadata(filepath="data/oracle_metadata.json"):
    """Load metadata from JSON file"""
    if not os.path.exists(filepath):
        print(f"✗ Metadata file not found: {filepath}")
        print("Run 'python src/sample_metadata.py' or 'python src/extract_metadata.py' first")
        return None
    
    with open(filepath, 'r') as f:
        metadata = json.load(f)
    
    print(f"✓ Loaded metadata from {filepath}")
    return metadata


def main():
    # Load metadata
    metadata = load_metadata()
    if not metadata:
        return
    
    # Connect to Neo4j
    neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
    neo4j_password = os.getenv('NEO4J_PASSWORD', 'password123')
    
    builder = Neo4jGraphBuilder(neo4j_uri, neo4j_user, neo4j_password)
    
    try:
        builder.build_graph(metadata)
        print("\n✓ Success! Open Neo4j Browser at http://localhost:7474")
        print("  Try query: MATCH (t:Table) RETURN t LIMIT 25")
    finally:
        builder.close()


if __name__ == "__main__":
    main()
