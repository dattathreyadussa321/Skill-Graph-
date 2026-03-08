"""
Seed the Neo4j database with Skill Graph DAG data.

Usage:
    python seed_graph.py

Requires Neo4j to be running and .env configured.
"""
import os
import sys
import re

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RecommendationSystem.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from models.connection import get_graph


def load_cypher_file(filepath):
    """Parse a .cypher file into executable statements."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    statements = []
    for line in content.split(';'):
        cleaned = re.sub(r'//.*', '', line).strip()
        if cleaned:
            statements.append(cleaned + ';')
    return statements


def run_seed():
    graph = get_graph()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Load both seed files
    files = ['seed_skill_graph.cypher', 'seed_courses.cypher']
    statements = []
    for f in files:
        path = os.path.join(base_dir, f)
        if os.path.exists(path):
            stmts = load_cypher_file(path)
            print(f"  Loaded {len(stmts)} statements from {f}")
            statements.extend(stmts)

    print(f"\nRunning {len(statements)} total Cypher statements...")

    success = 0
    errors = 0
    for i, stmt in enumerate(statements, 1):
        try:
            graph.run(stmt)
            success += 1
        except Exception as e:
            errors += 1
            # Show first 80 chars of statement for context
            preview = stmt[:80].replace('\n', ' ')
            print(f"  [{i}] ERROR: {e}\n       Statement: {preview}...")

    print(f"\nDone: {success} succeeded, {errors} failed")

    # Validate DAG (no cycles)
    print("\nValidating DAG (checking for cycles)...")
    result = graph.run(
        "MATCH path = (s)-[:PREREQUISITE*]->(s) RETURN count(path) AS cycles"
    ).data()
    cycles = result[0]['cycles'] if result else 0
    if cycles == 0:
        print("  DAG is valid - no cycles detected!")
    else:
        print(f"  WARNING: {cycles} cycle(s) detected!")

    # Print summary
    print("\nGraph summary:")
    for label in ['Career', 'Knowledge', 'Tool', 'Platform', 'Framework', 'ProgramingLanguage']:
        count = graph.run(f"MATCH (n:{label}) RETURN count(n) AS c").data()[0]['c']
        print(f"  {label}: {count} nodes")

    course_count = graph.run("MATCH (n:Course) RETURN count(n) AS c").data()[0]['c']
    print(f"  Course: {course_count} nodes")

    prereq_count = graph.run(
        "MATCH ()-[r:PREREQUISITE]->() RETURN count(r) AS c"
    ).data()[0]['c']
    print(f"  PREREQUISITE relationships: {prereq_count}")

    need_count = graph.run(
        "MATCH ()-[r]->() WHERE type(r) STARTS WITH 'NEED_' RETURN count(r) AS c"
    ).data()[0]['c']
    print(f"  NEED_* relationships: {need_count}")

    teach_count = graph.run(
        "MATCH ()-[r]->() WHERE type(r) STARTS WITH 'TEACH_' RETURN count(r) AS c"
    ).data()[0]['c']
    print(f"  TEACH_* relationships: {teach_count}")

    require_count = graph.run(
        "MATCH ()-[r]->() WHERE type(r) STARTS WITH 'REQUIRE_' RETURN count(r) AS c"
    ).data()[0]['c']
    print(f"  REQUIRE_* relationships: {require_count}")


if __name__ == '__main__':
    run_seed()
