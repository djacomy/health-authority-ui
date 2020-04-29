build: .env
	docker-compose build

run:
	docker-compose up -d

test: build
	docker-compose ${compose.test} run --rm server pytest

prod:
	docker-compose ${compose.prod} up -d

clean:
	docker-compose down

distclean: clean
	\rm .env

compose.main = -f docker-compose.yml
compose.test = ${compose.main} -f docker-compose-test.yml
compose.prod = ${compose.main} -f docker-compose-prod.yml

.env:
	cp .env-template $@
