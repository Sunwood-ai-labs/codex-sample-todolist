---
id: installation
title: インストール
---

## インストール

```bash
git clone https://github.com/Sunwood-ai-labs/codex-sample-todolist.git
cd codex-sample-todolist
# Docker を使う場合
docker-compose up --build
# もしくはローカルで実行する場合
pip install -r requirements.txt
export FLASK_APP=app.py
flask run
```