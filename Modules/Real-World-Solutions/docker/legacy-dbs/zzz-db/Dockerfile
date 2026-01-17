# =============================================================================
# ZZZ Accounting Legacy Database
# =============================================================================
# The "CLEAN" database - well-structured schema with proper conventions
# This represents what good database design looks like
# =============================================================================

FROM postgres:15-alpine

# Copy initialization scripts
COPY init.sql /docker-entrypoint-initdb.d/01-init.sql

# Set locale for proper UTF-8 support
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Expose PostgreSQL port
EXPOSE 5432
