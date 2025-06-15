FROM node:16-alpine

WORKDIR /app

# Copy package files first (for better caching)
COPY package*.json ./

# Install root dependencies if they exist
RUN if [ -f package.json ]; then npm install; fi

# Copy and install backend dependencies
COPY backend/package*.json ./backend/
RUN cd backend && npm install

# Copy and install frontend dependencies  
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install

# Copy source code (node_modules should be excluded by .dockerignore)
COPY . .

# Build the frontend application
RUN cd frontend && npm run build

EXPOSE 3000 5000

# Start the backend server
CMD ["node", "backend/app.js"]