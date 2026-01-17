# =============================================================================
# React Frontend for ZZZ Accounting Merger Platform
# =============================================================================
# Multi-stage build for production-ready React application
# =============================================================================

FROM node:20-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:3001/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
