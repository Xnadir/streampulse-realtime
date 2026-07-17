.PHONY: run test docker clean

run:
	python app.py

test:
	python -m pytest tests/ -v

docker:
	docker-compose up --build

clean:
	rm -rf __pycache__ .pytest_cache
