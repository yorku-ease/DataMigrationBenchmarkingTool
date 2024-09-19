#!/bin/bash

# Find and kill resourcesConsumer.py
PROCESS_ID=$(ps aux | grep '[r]esourcesConsumer.py' | awk '{print $2}')
if [ -n "$PROCESS_ID" ]; then
  echo "Killing resourcesConsumer.py with PID $PROCESS_ID"
  kill -9 $PROCESS_ID
else
  echo "resourcesConsumer.py is not running"
fi

# Find and kill consumer.py
PROCESS_ID=$(ps aux | grep '[c]onsumer.py' | awk '{print $2}')
if [ -n "$PROCESS_ID" ]; then
  echo "Killing consumer.py with PID $PROCESS_ID"
  kill -9 $PROCESS_ID
else
  echo "consumer.py is not running"
fi
