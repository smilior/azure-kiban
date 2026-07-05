# リリース手順書(雛形)

## 前提条件
> 対象環境・権限・事前チェック項目を書く。
- 対象サービス: `<service-name>` / デプロイ先: `<environment>`
- 実行者に必要な権限: `<role/permission>`
- 事前確認: CI が green、直近バックアップが存在する

## リリース手順
> コピペ実行できるコマンドを上から順に書く。各コマンドに期待される出力を添える。
1. 対象コミットを確認する。
```bash
git fetch origin && git log origin/main --oneline -5
```
期待される出力: リリース対象コミットが先頭に表示される。

2. デプロイを実行する。
```bash
<deploy-command> --env <environment> --version <version>
```
期待される出力: `Deploy succeeded`。

3. デプロイ完了を待つ。
```bash
<status-command> --env <environment>
```
期待される出力: ステータスが `healthy` になる。

## 確認手順
> リリース後に何を見て成功と判断するかを書く。
```bash
curl -sS https://<host>/healthz
```
- 期待される出力: `{"status":"ok"}` かつ HTTP 200
- メトリクス: エラー率・レイテンシが直前15分と同水準
- ログ: `<log-query>` にエラー増加がない

## ロールバック手順
> リリース手順の各ステップに対応する巻き戻し方を書く。
1. 直前バージョンを特定する。
```bash
<status-command> --env <environment> --history
```
期待される出力: 1つ前のバージョン番号が表示される。

2. 直前バージョンへ戻す。
```bash
<deploy-command> --env <environment> --version <previous-version>
```
期待される出力: `Deploy succeeded`(旧バージョン)。

3. ロールバック後の健全性を確認する。
```bash
curl -sS https://<host>/healthz
```
期待される出力: `{"status":"ok"}` かつ HTTP 200。
