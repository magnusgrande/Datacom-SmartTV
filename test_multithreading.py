#!/usr/bin/env python3
"""
Test script to demonstrate multi-threading functionality.
This script creates multiple client connections to test that they can all
interact with the same TV state simultaneously.

This code was written by GitHub Copilot based on the provided server and client code.
"""

import socket
import threading
import time


def client_simulation(client_id, commands):
    """Simulate a client connecting and sending commands."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', 1238))
            print(f"Client {client_id} connected successfully")

            for command in commands:
                print(f"Client {client_id} sending: {command}")
                client_socket.sendall((command + "\n").encode())

                response = client_socket.recv(1024).decode().strip()
                print(f"Client {client_id} received: {response}")

                # Small delay between commands
                time.sleep(0.5)

    except Exception as e:
        print(f"Client {client_id} error: {e}")


def main():
    """Main test function."""
    print("Starting multi-client test...")
    print("Make sure the server is running on localhost:1238")
    print()

    # Wait a moment to ensure server is ready
    time.sleep(1)

    # Define different command sequences for different clients
    client_commands = {
        1: ["get", "set power on", "get", "set channel up", "get"],
        2: ["get", "set channel up", "get", "set channel down", "get"],
        3: ["get", "set power off", "get", "set power on", "get"]
    }

    # Create threads for multiple clients
    threads = []
    for client_id, commands in client_commands.items():
        thread = threading.Thread(
            target=client_simulation,
            args=(client_id, commands),
            name=f"TestClient-{client_id}"
        )
        threads.append(thread)

    # Start all client threads
    for thread in threads:
        thread.start()
        time.sleep(0.2)  # Stagger the connections slightly

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("\nAll test clients completed!")
    print("Check the server output to see how it handled multiple concurrent connections.")


if __name__ == "__main__":
    main()
