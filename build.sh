#!/usr/bin/env bash
# скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# установка зависимостей, сбор статики и применение миграций
make install && make collectstatic && make migrate
