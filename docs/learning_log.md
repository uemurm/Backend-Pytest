# Daily Journal

## 2026-02-13 Fri
* Replaced in-memory DB with PostgreSQL

## 2026-02-06 Fri
* 抜けているテスト項目を洗い出した。

## 2026-01-26 Mon Australia Day
* Updated workflow file to run tests on GitHub Actions using Docker Compose.

## 2026-01-23 Fri
* Created another container for pytest as well.

## 2026-01-22 Thu 
* Use Docker compose on top of Docker.
* Add tests of requests resulting in errors.

### Key Takeaways
GitHub Actions での実行環境の詳細:
* `runs-on: ubuntu-latest`で指定してるのは仮想マシン。独自のカーネルを持ち、Python や Docker エンジンを持っている。
* `docker run`で上記の上にコンテナが作成され、仮想マシンのカーネルを借りて動く。

## 2026-01-21 Wed
* Dockerise API server
ローカルマシンで実行していた API サーバを、Docker コンテナ上でも実行できるようにした。
'It ran on my machine' problem. を避けたり、テスト環境をサッと作って、テストが終わったらコンテナを停止して環境を捨てる事ができる。

## 2026-01-17 Update README

### 🎯 Goal
- Verify the startup instructions in the README.md.
- Update the file accordingly.
- Set up GitHub Actions to run tests when pushing.

### 📝 Notes
- git cloned and ran tests from scratch.
- Set up GitHub Actions and confirmed all passed except test_dummyjson.
- Refactored test_dummyjson.py by replacing jsonschema with Pydantic and confirmed all passed locally.

### Clean-up
- Deleted dummyJson_product.schema.json file as it's no longer necessary.

### 🚧 Challenges & Solutions
- **Problem**: `ModuleNotFoundError: No module named 'jsonschema'`
- **Solution**: Added Todo below instead of `uv add jsonschema` to add the missing dependency.

# Todo's
- [x] Dockerise pytest as well.
- [x] Run tests on GitHub Actions using Docker Compose 
- [X] Refactor test_dummyjson_product.py by replacing jsonschema with Pydantic.
