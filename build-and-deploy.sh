#!/bin/bash

# Industrial Energy Dashboard - Build and Deploy Script
# This script automates the data pipeline, container rebuild, and deployment process

set -e  # Exit on any error

# Configuration
ENVIRONMENT=${1:-local}  # local, staging, production
FORCE_REBUILD=${2:-false}

echo "🚀 Starting Industrial Energy Dashboard build and deploy process..."
echo "Environment: $ENVIRONMENT"
echo "Force rebuild: $FORCE_REBUILD"

# Function to check if data has changed
check_data_changes() {
    echo "📊 Checking for data changes..."
    
    # Check if raw data files have been modified recently (last 24 hours)
    if find ./data/raw -name "*.csv" -mtime -1 | grep -q .; then
        echo "✅ Recent data changes detected"
        return 0
    elif [ "$FORCE_REBUILD" = "true" ]; then
        echo "✅ Force rebuild requested"
        return 0
    else
        echo "ℹ️  No recent data changes found"
        return 1
    fi
}

# Function to run data pipeline
run_data_pipeline() {
    echo "🔄 Running data pipeline..."
    
    # Stop existing services
    echo "Stopping existing services..."
    docker-compose down
    
    # Build and run data services
    echo "Building data services..."
    docker-compose build industrialenergy_data industrialenergy_datapipeline
    
    # Start data server
    echo "Starting data server..."
    docker-compose up -d industrialenergy_data
    
    # Wait for data server to be ready
    echo "Waiting for data server..."
    sleep 10
    
    # Run pipeline
    echo "Running data pipeline..."
    docker-compose run --rm industrialenergy_datapipeline
    
    echo "✅ Data pipeline completed"
}

# Function to build dashboard
build_dashboard() {
    echo "🏗️  Building dashboard..."
    
    # Build dashboard image
    docker-compose build industrialenergy_dashboard
    
    echo "✅ Dashboard build completed"
}

# Function to deploy based on environment
deploy() {
    echo "🚀 Deploying to $ENVIRONMENT..."
    
    case $ENVIRONMENT in
        "local")
            deploy_local
            ;;
        "staging")
            deploy_staging
            ;;
        "production")
            deploy_production
            ;;
        *)
            echo "❌ Unknown environment: $ENVIRONMENT"
            exit 1
            ;;
    esac
}

# Local deployment
deploy_local() {
    echo "🏠 Starting local deployment..."
    
    # Set local environment variables
    export DASH_BASE_PATHNAME=/
    export DATA_DIR=/app/data/final
    
    # Start services (excluding pipeline to avoid conflicts)
    docker-compose up -d industrialenergy_data industrialenergy_dashboard
    
    echo "✅ Local deployment completed"
    echo "🌐 Dashboard available at: http://localhost:3009"
}

# Staging deployment
deploy_staging() {
    echo "🔧 Starting staging deployment..."
    
    # Set staging environment variables
    export DASH_BASE_PATHNAME=/staging/dashboard/
    export DATA_DIR=/app/data/final
    
    # Start services
    docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d industrialenergy_data industrialenergy_dashboard
    
    echo "✅ Staging deployment completed"
}

# Production deployment
deploy_production() {
    echo "🏭 Starting production deployment..."
    
    # Set production environment variables  
    export DASH_BASE_PATHNAME=/capstone/industrialenergy/dashboard/
    export DATA_DIR=/capstone/industrialenergy/dashboard/data/final
    
    # Tag images for production
    docker tag industrialenergy_dashboard:latest industrialenergy_dashboard:production
    docker tag industrialenergy_data:latest industrialenergy_data:production
    
    # Start production services
    docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d industrialenergy_data industrialenergy_dashboard
    
    echo "✅ Production deployment completed"
}

# Function to run health checks
health_check() {
    echo "🏥 Running health checks..."
    
    # Wait for services to start
    sleep 15
    
    # Check dashboard health
    if curl -f http://localhost:3009/ > /dev/null 2>&1; then
        echo "✅ Dashboard is healthy"
    else
        echo "❌ Dashboard health check failed"
        return 1
    fi
    
    # Check data server health
    if curl -f http://localhost:3010/ > /dev/null 2>&1; then
        echo "✅ Data server is healthy"
    else
        echo "❌ Data server health check failed"
        return 1
    fi
    
    echo "✅ All health checks passed"
}

# Main execution flow
main() {
    echo "Starting build and deploy process..."
    
    # Check if we need to rebuild
    if check_data_changes; then
        run_data_pipeline
        build_dashboard
    else
        echo "ℹ️  Skipping pipeline - no data changes detected"
        echo "💡 Use './build-and-deploy.sh $ENVIRONMENT true' to force rebuild"
        
        # Still rebuild dashboard if it doesn't exist
        if ! docker images | grep -q industrialenergy_dashboard; then
            echo "🏗️  Dashboard image not found, building..."
            build_dashboard
        fi
    fi
    
    # Deploy
    deploy
    
    # Health check
    health_check
    
    echo "🎉 Build and deploy completed successfully!"
    echo "📊 Dashboard URL: http://localhost:3009"
    echo "📈 Data server URL: http://localhost:3010"
}

# Help function
show_help() {
    echo "Industrial Energy Dashboard - Build and Deploy Script"
    echo ""
    echo "Usage: $0 [ENVIRONMENT] [FORCE_REBUILD]"
    echo ""
    echo "ENVIRONMENT:"
    echo "  local       - Local development (default)"
    echo "  staging     - Staging environment"
    echo "  production  - Production environment"
    echo ""
    echo "FORCE_REBUILD:"
    echo "  true        - Force rebuild even if no data changes"
    echo "  false       - Only rebuild if data changes (default)"
    echo ""
    echo "Examples:"
    echo "  $0                          # Local deployment, auto-detect changes"
    echo "  $0 local true               # Local deployment, force rebuild"
    echo "  $0 production               # Production deployment, auto-detect changes"
    echo "  $0 staging true             # Staging deployment, force rebuild"
}

# Parse command line arguments
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    show_help
    exit 0
fi

# Run main function
main 