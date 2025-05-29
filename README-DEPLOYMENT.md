# 🚀 Deployment Guide

## Safe Commands (Prevent Conflicts)

### When you have new data:
```bash
# 1. Process the data (runs once and stops)
docker-compose --profile pipeline run --rm industrialenergy_datapipeline

# 2. Start the dashboard
docker-compose up -d industrialenergy_data industrialenergy_dashboard
```

### For production (in .env set environment variables first):
```bash
# Set production paths
export DASH_BASE_PATHNAME=/capstone/industrialenergy/dashboard/
export DATA_DIR=/capstone/industrialenergy/dashboard/data/final

# Then run the same commands
docker-compose --profile pipeline run --rm industrialenergy_datapipeline
docker-compose up -d industrialenergy_data industrialenergy_dashboard
```

## Safety Features ✅

- **Pipeline requires explicit profile** (prevents accidental conflicts)
- **Data Pipeline service automatically stops** after processing data  
- **`docker-compose up` only starts data server + dashboard** (safe)
- **Clear separation** between data processing and app serving

## Quick Reference

- **Local dashboard**: http://localhost:3009
- **Check logs**: `docker-compose logs industrialenergy_dashboard`  
- **Stop everything**: `docker-compose down`
- **Rebuild**: `docker-compose build`

## What Each Command Does

- **`docker-compose --profile pipeline run --rm industrialenergy_datapipeline`**: Runs data processing (stops all when done)
- **`docker-compose up`**: Runs data server + dashboard (safe default)
- **`docker-compose build`**: Builds all services (now works!)

## Useful Commands for Debugging & Management

### 🔍 **Debugging & Inspection**
```bash
# Get inside running dashboard container
docker exec -it dashboard-industrialenergy_dashboard-1 /bin/bash

# Get inside running data server
docker exec -it dashboard-industrialenergy_data-1 /bin/bash

# View real-time logs (dashboard)
docker-compose logs -f industrialenergy_dashboard

# View real-time logs (data server)  
docker-compose logs -f industrialenergy_data

# View all logs from last run
docker-compose logs

# Check what's running
docker ps

# See all containers (including stopped)
docker ps -a
```

### 📊 **Monitoring & Status**
```bash
# Check container resource usage
docker stats

# Check service health and ports
docker-compose ps

# Test dashboard connectivity
curl http://localhost:3009

# Test data server connectivity
curl http://localhost:3010

# See disk usage by containers
docker system df
```

### 🔧 **Management & Cleanup**
```bash
# Stop specific service
docker-compose stop industrialenergy_dashboard

# Restart specific service
docker-compose restart industrialenergy_dashboard

# Force rebuild single service
docker-compose build --no-cache industrialenergy_dashboard

# Remove stopped containers and networks
docker-compose down

# Nuclear option: stop everything and clean up
docker-compose down && docker system prune -f

# Remove unused images (frees disk space)
docker image prune
```

### 📁 **File Operations**
```bash
# Copy file from container to local
docker cp dashboard-industrialenergy_dashboard-1:/app/data/final/iac_integrated.csv ./

# Copy file from local to container
docker cp ./new_data.csv dashboard-industrialenergy_dashboard-1:/app/data/final/

# Check file sizes inside container
docker exec dashboard-industrialenergy_dashboard-1 ls -lh /app/data/final/

# Check disk space inside container
docker exec dashboard-industrialenergy_dashboard-1 df -h
```

### 🏥 **Troubleshooting**
```bash
# If dashboard won't start - check what's using port 3009
lsof -i :3009

# Kill process using port 3009 (if needed)
kill -9 $(lsof -t -i:3009)

# View container startup command
docker inspect dashboard-industrialenergy_dashboard-1 | grep -A 10 "Cmd"

# Check environment variables inside container
docker exec dashboard-industrialenergy_dashboard-1 env | grep -E "(DASH|DATA)"

# Manual data processing (if pipeline fails)
docker-compose run --rm industrialenergy_datapipeline
```

## Recommended Approach

### Keep your main services running
docker-compose up -d industrialenergy_data industrialenergy_dashboard

### Run pipeline when needed (without affecting other services)
docker-compose --profile pipeline run --rm industrialenergy_datapipeline
