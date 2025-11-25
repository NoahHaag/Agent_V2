from tools_2 import gmail_read_tool_for_agent
import json

def test_gmail_tool():
    print("Testing gmail_read_tool_for_agent...")
    
    # Test 1: Broad search (should return something if inbox is not empty)
    query1 = "label:inbox"
    print(f"\nTest 1: Query='{query1}'")
    try:
        result1 = gmail_read_tool_for_agent.func(query=query1, max_results=3)
        print(json.dumps(result1, indent=2))
    except Exception as e:
        print(f"Test 1 Failed: {e}")

    # Test 2: Specific sender (ecolog-l)
    query2 = "from:ecolog-l label:inbox"
    print(f"\nTest 2: Query='{query2}'")
    try:
        result2 = gmail_read_tool_for_agent.func(query=query2, max_results=3)
        print(json.dumps(result2, indent=2))
    except Exception as e:
        print(f"Test 2 Failed: {e}")

if __name__ == "__main__":
    test_gmail_tool()
