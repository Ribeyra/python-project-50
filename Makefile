install: # Установка зависимостей с использованием poetry
	poetry install

gendiff-h: # Запуск "gendiff -h"
	poetry run gendiff -h

build: # Сборка пакета с использованием poetry
	poetry build

publish: # Опубликовать пакет ("сухой запуск" без фактической публикации)
	poetry publish --dry-run

package-install: # Установка пакета из собранных файлов
	python3 -m pip install --user dist/*.whl

package-uninstall: # Удаление установленного пакета
	python3 -m pip uninstall hexlet-code

lint: # Запуск flake8 для проверки стиля кода в проекте
	poetry run flake8 gendiff

test: # Запуск тестов
	poetry run pytest

cov-test: # Проверка покрытия кода тестами
	poetry run pytest --cov
	poetry run coverage report -m
