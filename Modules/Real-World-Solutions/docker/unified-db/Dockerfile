# =============================================================================
# Unified Database - Merged Clean Data
# =============================================================================
# The target database where all cleaned and normalized data will be loaded.
# This represents the properly designed merged entity database.
# =============================================================================

FROM postgres:15-alpine

# Copy initialization scripts
COPY schema.sql /docker-entrypoint-initdb.d/01-schema.sql

# Set locale for proper UTF-8 support
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Expose PostgreSQL port
EXPOSE 5432
