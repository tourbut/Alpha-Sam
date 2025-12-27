# Build stage
FROM node:20-slim as builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build
RUN npm prune --production

# Final stage
FROM node:20-slim

WORKDIR /app

# Copy built assets and dependencies
COPY --from=builder /app/build build/
COPY --from=builder /app/node_modules node_modules/
COPY package.json .

EXPOSE 3000

ENV NODE_ENV=production
# adapter-node defaults to listening on port 3000
CMD ["node", "build"]

