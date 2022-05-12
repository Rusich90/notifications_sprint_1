include .env

first-up:
	@docker-compose up -d
	@make create-users-table
	@make load-dump

create-users-table:
	@echo "\n\033[01;33m Create users table\033[0m"
	@./bin/postgres-check
	@docker-compose exec -T db psql -U "${POSTGRES_USER}" "${POSTGRES_DB}" -c "CREATE TABLE IF NOT EXISTS users (id UUID PRIMARY KEY, first_name VARCHAR, last_name VARCHAR, email VARCHAR, email_verified BOOLEAN DEFAULT FALSE);"

load-dump:
	@echo "\n\033[01;33m Load  dump\033[0m"
	@docker-compose exec -T db psql -U "${POSTGRES_USER}" "${POSTGRES_DB}" < dump.sql
