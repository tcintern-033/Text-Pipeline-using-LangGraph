from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# Define the State
class TextProcessingState(TypedDict, total=False):
    raw_input: str
    cleaned_text: str
    word_count: int
    final_status: str

# Node 1: Cleaner
def cleaner_node(state: TextProcessingState):
    print("--- Executing Node 1: Cleaner ---")
    raw = state.get("raw_input", "")
    
    # Strip whitespace and standardize casing to lowercase
    cleaned = raw.strip().lower()
    
    return {"cleaned_text": cleaned}

# Node 2: Analyzer
def analyzer_node(state: TextProcessingState):
    print("--- Executing Node 2: Analyzer ---")
    cleaned = state.get("cleaned_text", "")
    
    # Calculate word count
    word_count = len(cleaned.split())
    
    return {"word_count": word_count}

# Node 3: Formatter
def formatter_node(state: TextProcessingState):
    print("--- Executing Node 3: Formatter ---")
    word_count = state.get("word_count", 0)
    
    # Generate final status string based on the analysis
    status = f"Successfully processed text! Total word count: {word_count}."
    if word_count == 0:
        status += " (Warning: The input text was empty!)"
        
    return {"final_status": status}

# Build the Graph
workflow = StateGraph(TextProcessingState)

# Add Nodes
workflow.add_node("cleaner", cleaner_node)
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("formatter", formatter_node)

# Add Edges (Linear Flow)
workflow.add_edge(START, "cleaner")
workflow.add_edge("cleaner", "analyzer")
workflow.add_edge("analyzer", "formatter")
workflow.add_edge("formatter", END)

# Compile the Graph
app = workflow.compile()

if __name__ == "__main__":
    print("==================================================")
    print("Starting Deterministic Text Processing Pipeline")
    print("==================================================\n")
    
    raw_input_text = input("Enter your raw input: ")

    # The initial state contains just the raw input string
    initial_state = {
        "raw_input": raw_input_text
    }
    
    print(f"[Initial State]:\n{initial_state}\n")
    print("-" * 50)
    
    # Stream the execution to observe state mutations
    for step_output in app.stream(initial_state):
        for node_name, state_update in step_output.items():
            print(f"\n[Update from '{node_name}']:")
            print(f"Mutations: {state_update}\n")
            print("-" * 50)
            
    print("\nWorkflow Execution Complete!")
