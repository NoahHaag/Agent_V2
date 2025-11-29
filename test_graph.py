import sys
import os

# Add project root to path
sys.path.append(r"d:\Python Projects\AI Agents\Agent_V2")

from tools_2 import generate_network_graph, add_cold_email

# Add a test referral to existing data (non-destructive as it updates existing or adds new)
# We'll add a dummy referral to one of the existing contacts if possible, or just print the current graph
print("Generating graph from current data...")
graph_code = generate_network_graph()
print("\n--- Mermaid Graph Code ---\n")
print(graph_code)
print("\n--------------------------\n")

if "graph TD" in graph_code:
    print("✅ Graph generation successful!")
else:
    print("❌ Graph generation failed.")
