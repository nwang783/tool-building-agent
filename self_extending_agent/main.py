"""
Main entry point for the self-extending tool system.
"""
import asyncio
import os
from dotenv import load_dotenv

from agents import Runner #type: ignore[import]

# Import from self_extending_agent\dev_agents\triage_agent.py
from dev_agents.triage_agent import triage_agent

# Load environment variables
load_dotenv()

async def main():
    """Run the self-extending tool system."""
    print("Starting Self-Extending Tool System...")
    
    while True:
        # Get user input
        user_input = input("\nEnter your request (or 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            break
        
        # Run the triage agent
        try:
            result = await Runner.run(triage_agent, user_input)
            
            # Display the result
            print("\nAgent Response:")
            print(result.final_output)
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
    