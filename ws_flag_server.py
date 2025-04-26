#!/usr/bin/env python

import asyncio
import websockets
import json
import time
import random

# Dictionary of flags that can be toggled
flags = {
    'violence': False,
    'air_safety': False,
    'health': False,
    'distraction': False,
    'drowsiness': False,
    'lane_departure': False,
    'emotion': False,
    'blind_spot_left': False,
    'blind_spot_right': False,
    'up_arrow': False,
    'left_arrow': False,
    'down_arrow': False,
    'right_arrow': False,
    'brakes': False
}

connected_clients = set()

async def handler(websocket):
    """Handle a connection and dispatch it to the right handler."""
    print("Client connected")
    connected_clients.add(websocket)
    
    try:
        # Send initial state
        await websocket.send(json.dumps(flags))
        
        # Keep the connection alive and handle any received messages
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received: {data}")
                
                # Handle subscription message
                if 'type' in data and data['type'] == 'subscribe':
                    print(f"Client subscribed to {data.get('channel', 'unknown')}")
                    
                # Handle flag toggle messages
                if 'toggle' in data and data['toggle'] in flags:
                    flag = data['toggle']
                    value = data.get('value', not flags[flag])  # Toggle or set to specified value
                    flags[flag] = value
                    print(f"Flag {flag} set to {value}")
                    
                    # Broadcast to all clients
                    await broadcast({flag: value})
            except json.JSONDecodeError:
                print(f"Invalid JSON: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
    finally:
        connected_clients.remove(websocket)

async def broadcast(data):
    """Broadcast data to all connected clients."""
    if connected_clients:
        await asyncio.gather(
            *[client.send(json.dumps(data)) for client in connected_clients]
        )

async def toggle_random_flags():
    """Randomly toggle flags for demonstration purposes."""
    while True:
        await asyncio.sleep(5)  # Toggle a random flag every 5 seconds
        flag = random.choice(list(flags.keys()))
        flags[flag] = not flags[flag]
        print(f"Randomly toggled {flag} to {flags[flag]}")
        await broadcast({flag: flags[flag]})

async def interactive_console():
    """Allow manual toggling of flags through console input."""
    while True:
        print("\nAvailable flags:")
        for i, flag in enumerate(flags.keys(), 1):
            print(f"{i}. {flag}: {flags[flag]}")
        print("Enter flag number to toggle, or 'q' to quit:")
        
        # Use asyncio to read from stdin without blocking
        loop = asyncio.get_event_loop()
        choice = await loop.run_in_executor(None, input)
        
        if choice.lower() == 'q':
            print("Exiting interactive console")
            break
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(flags):
                flag = list(flags.keys())[index]
                flags[flag] = not flags[flag]
                print(f"Toggled {flag} to {flags[flag]}")
                await broadcast({flag: flags[flag]})
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")

async def main():
    print("WebSocket Flag Server starting...")
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        # Run both tasks concurrently
        await asyncio.gather(
            toggle_random_flags(),
            interactive_console()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user")