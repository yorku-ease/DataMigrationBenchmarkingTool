        # Define the container name or ID
        CONTAINER_NAME_OR_ID="$1"
        
        # Define the maximum number of attempts
        MAX_ATTEMPTS=10
        
        # Define the interval between attempts in seconds
        INTERVAL=5
        
        # Loop to check the health status
        for ((i = 1; i <= MAX_ATTEMPTS; i++)); do
            # Use docker inspect to get the health status in JSON format
            HEALTH=$(docker inspect --format='{{json .State.Health}}' "$CONTAINER_NAME_OR_ID")
        
            # Extract the "Status" field from the JSON
            STATUS=$(echo "$HEALTH" | jq -r '.Status')
        
            # Check if the container is healthy
            if [ "$STATUS" == "healthy" ]; then
                echo "Container is healthy!"
                exit 0
            elif [ "$STATUS" == "unhealthy" ]; then
                echo "Container is unhealthy!"
                exit 1  # Return 1 for unhealthy
            else
                echo "Attempt $i: Container is still starting. Waiting for $INTERVAL seconds... $STATUS"
                sleep "$INTERVAL"
            fi
        done
        
        # If maximum attempts are reached and the container is still starting, exit with an error code
        echo "Maximum attempts reached. Unable to determine health status."
        exit 255
