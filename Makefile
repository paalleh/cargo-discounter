.PHONY: up down build

build:
	docker-compose -f docker-compose.prod.yml build

up:
	docker-compose -f docker-compose.dev.yml up -d

down:
	docker-compose -f docker-compose.prod.yml down -v
