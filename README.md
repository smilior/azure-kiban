# ai-dev-template — AI駆動開発テンプレート

社内システムを AI 駆動(TDD)で開発するためのテンプレート。標準文書・書類雛形・専門エージェント定義を1つのリポジトリに揃えている。

**文書サイト**: https://smilior.github.io/ai-dev-template/

## なに(What)

- **docs-template/standards/** — 開発標準・統制規程・チーム名鑑・成果物ガイド(HTML は GitHub Pages で配信)
- **docs-template/project/** — 案件書類の雛形11本(企画書〜障害記録。記入ガイドと記入例入り)
- **docs/** — 実際の案件書類を置く場所(雛形を docs-template/ からコピーして記入する)
- **.claude/agents/** — 書類担当の専門エージェント定義10体(Sonnet 5)
- **CLAUDE.md** — 開発規約と TDD ガードレール
- **tools/md2html.py** — Markdown 正本から配布用 HTML を生成するスクリプト

## なぜ(Why)

書類の目次・規約・エージェントへの指示を案件のたびに作り直さないため。正本は Markdown(AI が読む)、配布は HTML(人が読む)に分け、承認は PR マージで記録する。

## だれ(Who)

- **指示者**: Claude Code。作業を分解して専門エージェントに委任し、成果物を検品する
- **あなた(社内SE)**: 題材と優先順位を決め、PR をマージする
- **利用部門**: 要件の確認と UAT([協力ガイド](https://smilior.github.io/ai-dev-template/standards/cooperation-guide.html))
- **上長**: 規程とリリースの承認([承認ガイド](https://smilior.github.io/ai-dev-template/standards/approval-guide.html))

## いつ・どう使う(When / How)

### 使い始める(案件リポジトリの複製)

このリポジトリは GitHub のテンプレートになっている。案件を始めるときは複製する(履歴なしのまっさらな状態で始まる):

```bash
gh repo create smilior/<案件名> --template smilior/ai-dev-template --private --clone
cd <案件名> && claude   # →「◯◯を作りたい。企画書から始めて」
```

GitHub の画面なら「Use this template」ボタンでも同じ。複製した先での調整は3つ:

1. **docs-template/standards/ は削除してよい** — 正本はテンプレート側にあり、閲覧は文書サイトでできる。残すと改訂が追いかけてこない古いコピーになる
2. **.github/workflows/pages.yml を削除する** — 案件リポジトリは private のため Pages は動かない
3. **CLAUDE.md の「案件確定時に記入」欄** — スタック決定後に tech-lead に任せる

### 開発の回し方

複製したら、次の3手で回す。

1. **題材を伝える** — Claude Code に「◯◯を管理するシステムを作りたい」
2. **確認事項に答える** — エージェントは業務ルールを勝手に決めず、質問リストで返してくる
3. **PR をマージする** — マージ = 承認記録。docs/ とコードが1段ずつ育つ

最初に読む3枚: [ポータル](https://smilior.github.io/ai-dev-template/standards/index.html) → [ライフサイクル標準](https://smilior.github.io/ai-dev-template/standards/ai-driven-dev-lifecycle.html) → [統制規程](https://smilior.github.io/ai-dev-template/standards/governance.html)

## どこで(Where)

- 文書の閲覧: 上記の文書サイト(main へのマージで自動更新)
- 文書の編集: Markdown 正本を PR で変更する。HTML は `tools/md2html.py` で生成する(直接編集しない)

```bash
python3 tools/md2html.py docs-template/standards/governance.md \
  -o docs-template/standards/governance.html \
  --docno STD-AIDEV-003 --rev 1.1 --date 2026-07-04
```

## 問い合わせ

情報システム担当(m_nakagawa@smilior.com)
