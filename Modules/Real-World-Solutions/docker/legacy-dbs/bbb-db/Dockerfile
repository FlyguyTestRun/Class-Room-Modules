# =============================================================================
# BBB Construction Legacy Database
# =============================================================================
# The "DIFFERENT" database - completely different schema design using
# UUIDs, JSON columns, and construction industry terminology.
# =============================================================================

FROM postgres:15-alpine

# Copy initialization scripts
COPY init.sql /docker-entrypoint-initdb.d/01-init.sql

# Set locale for proper UTF-8 support
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Expose PostgreSQL port
EXPOSE 5432
