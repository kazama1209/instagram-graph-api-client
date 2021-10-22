# instagram-graph-api-client

詳細はQiitaにて記載。

https://qiita.com/kazama1209/items/ac3eed4247eda4009b51

## セットアップ

```
$ cd python
$ cp .env.example .env

BUSINESS_ACCOUNT_ID=<InstagramのビジネスアカウントID>
ACCESS_TOKEN=<アクセストークン>
```

## 動作確認

```
$ docker-compose up -d
$ docker exec -it python3 /bin/bash
$ python main.py
```
