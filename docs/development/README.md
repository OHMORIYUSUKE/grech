# 開発

## このコードを自身でビルドして使いたい方、コードを編集して使いたい方へ

### ソースコードを編集

開発は Docker を用いて行えるようになっています。
Python のパッケージマネージャである Poetry を用いています。

```sh
# dockerコンテナを立ち上げる
$ docker compose up -d
# dockerコンテナに入る
$ docker exec -it grech bash
# 必要なライブラリをインストールする
$ poetry install
# grechコマンドをコンテナ内で実行できます
$ poetry run grech
```

### フォーマット

フォーマッタは black を用いています。

```sh
# フォーマットします
$ poetry run black .
```

### ビルド

```sh
$ poetry build
```

`sdist`内に`.tar.gz`と`.whl`が生成されます。
