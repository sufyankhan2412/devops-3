
echo "Starting Selenium Tests for Task Manager App..."

# Create necessary directories
mkdir -p test-results screenshots

# Build and run tests
docker-compose -f docker-compose.test.yml down --remove-orphans
docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml up --abort-on-container-exit

# Copy test results
echo "Test execution completed. Check test-results/ for reports."

# Cleanup
docker-compose -f docker-compose.test.yml down --remove-orphans
