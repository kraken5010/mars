up:
	docker-compose up -d --build

migrate:
	docker-compose exec web python manage.py migrate

superuser:
	docker-compose exec web python manage.py createsuperuser

down:
	docker-compose down && docker network prune --force

# Get project in docker
# docker exec -t -i <<container_id>> bash