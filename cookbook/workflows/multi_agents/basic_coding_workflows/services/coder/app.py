from floki import CoderAgent
from dotenv import load_dotenv
import asyncio
import logging

async def main():
    try:
        # Define Agent
        coder_agent = CoderAgent(
            name="CoderAgent",
            role="Code Generator",
            message_bus_name="messagepubsub",
            state_store_name="agenticworkflowstate",
            state_key="workflow_state",
            agents_registry_store_name="agentsregistrystore",
            agents_registry_key="agents_registry",
            service_port=8001,
            daprGrpcPort=50001
        )
        
        await coder_agent.start()
    except Exception as e:
        print(f"Error starting service: {e}")

if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(level=logging.INFO)
    
    asyncio.run(main())