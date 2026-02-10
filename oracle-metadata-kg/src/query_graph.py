"""
Query the Neo4j knowledge graph using LangChain and OpenAI.
Allows natural language queries about the database schema.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.prompts import PromptTemplate

load_dotenv()


class GraphQueryAgent:
    def __init__(self):
        # Initialize Neo4j connection
        self.graph = Neo4jGraph(
            url=os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
            username=os.getenv('NEO4J_USER', 'neo4j'),
            password=os.getenv('NEO4J_PASSWORD', 'password123')
        )
        
        # Initialize OpenAI
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4",
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Create custom prompt for better Cypher generation
        cypher_prompt = PromptTemplate(
            template="""You are a Neo4j expert. Given an input question, create a syntactically correct Cypher query.
            
Schema:
{schema}

The schema contains:
- Table nodes with properties: name, owner, tablespace, num_rows
- Column nodes with properties: name, data_type, nullable, data_length, position
- Index nodes with properties: name, type, uniqueness, columns
- Constraint nodes with properties: name, type, columns

Relationships:
- (Table)-[:HAS_COLUMN]->(Column)
- (Table)-[:HAS_INDEX]->(Index)
- (Table)-[:HAS_CONSTRAINT]->(Constraint)
- (Table)-[:HAS_FOREIGN_KEY]->(Table)
- (Index)-[:INDEXES_COLUMN]->(Column)

Only use relationship types and properties that exist in the schema.
Do not use any other relationship types or properties.

Question: {question}

Cypher Query:""",
            input_variables=["schema", "question"]
        )
        
        # Create the QA chain
        self.qa_chain = GraphCypherQAChain.from_llm(
            llm=self.llm,
            graph=self.graph,
            verbose=True,
            cypher_prompt=cypher_prompt,
            return_intermediate_steps=True
        )
        
        print("✓ Graph Query Agent initialized")
    
    def query(self, question):
        """Query the graph using natural language"""
        try:
            result = self.qa_chain.invoke({"query": question})
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def run_cypher(self, cypher_query):
        """Run a raw Cypher query"""
        try:
            result = self.graph.query(cypher_query)
            return result
        except Exception as e:
            return {"error": str(e)}


def print_result(result):
    """Pretty print query results"""
    if "error" in result:
        print(f"\n✗ Error: {result['error']}")
        return
    
    print("\n" + "="*60)
    
    if "intermediate_steps" in result:
        print("\nGenerated Cypher Query:")
        print("-" * 60)
        cypher = result['intermediate_steps'][0]['query']
        print(cypher)
        
        print("\nDatabase Results:")
        print("-" * 60)
        db_result = result['intermediate_steps'][0]['context']
        if db_result:
            for item in db_result:
                print(item)
        else:
            print("No results found")
    
    print("\nFinal Answer:")
    print("-" * 60)
    print(result.get('result', 'No answer generated'))
    print("="*60 + "\n")


def interactive_mode():
    """Run in interactive query mode"""
    print("\n" + "="*60)
    print("Oracle Metadata Knowledge Graph - Query Interface")
    print("="*60)
    print("\nInitializing...")
    
    agent = GraphQueryAgent()
    
    print("\nReady! Ask questions about your database schema.")
    print("Type 'exit' to quit, 'cypher' to run raw Cypher queries.\n")
    
    example_questions = [
        "Show me all tables",
        "What columns does the EMPLOYEES table have?",
        "Which tables have foreign keys?",
        "Find all indexes on the EMPLOYEES table",
        "What tables have more than 5 columns?",
        "Show me the relationships between EMPLOYEES and DEPARTMENTS"
    ]
    
    print("Example questions:")
    for i, q in enumerate(example_questions, 1):
        print(f"  {i}. {q}")
    print()
    
    while True:
        try:
            question = input("Your question: ").strip()
            
            if not question:
                continue
            
            if question.lower() == 'exit':
                print("Goodbye!")
                break
            
            if question.lower() == 'cypher':
                print("\nEnter Cypher query (or 'back' to return):")
                cypher = input("Cypher> ").strip()
                if cypher.lower() != 'back':
                    result = agent.run_cypher(cypher)
                    print("\nResults:")
                    print(result)
                continue
            
            print("\nProcessing...")
            result = agent.query(question)
            print_result(result)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}\n")


def run_example_queries():
    """Run some example queries"""
    print("\n" + "="*60)
    print("Running Example Queries")
    print("="*60)
    
    agent = GraphQueryAgent()
    
    queries = [
        "How many tables are in the database?",
        "What are the names of all tables?",
        "Show me all columns in the EMPLOYEES table",
        "Which tables have foreign key relationships?"
    ]
    
    for i, question in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] Question: {question}")
        result = agent.query(question)
        print_result(result)
        input("Press Enter to continue...")


def main():
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--examples':
            run_example_queries()
        elif sys.argv[1] == '--query':
            if len(sys.argv) > 2:
                question = ' '.join(sys.argv[2:])
                agent = GraphQueryAgent()
                result = agent.query(question)
                print_result(result)
            else:
                print("Usage: python src/query_graph.py --query <your question>")
        else:
            print("Usage:")
            print("  python src/query_graph.py              # Interactive mode")
            print("  python src/query_graph.py --examples   # Run example queries")
            print("  python src/query_graph.py --query <question>")
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
