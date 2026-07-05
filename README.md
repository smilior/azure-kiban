# azure-kiban — Azureアプリ公開基盤(検証)

社内研究テーマ「アイデア探求ワーク」の検証案件。AI駆動開発で構築したアプリを、Azure上の社内閉域網で短時間で公開できる基盤(静的・動的の2種)を構築し、現行のVM運用と実測で比較する。

**文書サイト**: https://smilior.github.io/azure-kiban/

## なに(What)

- **docs/project/** — 案件文書の正本(Markdown)。企画書・要件定義書・用語集・ADR
- **docs-html/** — 閲覧用の配布HTML。GitHub Pagesで上記サイトとして配信する
- **docs-template/** — 標準文書と書類雛形の原本(複製元テンプレート由来)
- **.claude/agents/** — 書類担当の専門エージェント定義10体
- **CLAUDE.md** — 開発規約とTDDガードレール

## いま(Status)

検討フェーズ。企画書と要件定義書(9ストーリー・23シナリオ)は起案済み。認証方式はADR-0002で決定済み(Easy Auth + Microsoft Entra ID)。環境パターンはADR-0001で比較中(P1: App Service集約が推奨)。

## 決めごと(Rules)

- 正本はMarkdown、HTMLは配布物。編集は必ずMarkdown側で行い、HTMLを再生成する
- 文書の変更はPRで行う。マージ=承認記録
- 検証は2段階。第1段=テンプレートから環境構築・公開・実測、第2段=自動デプロイ・SSO・複数アプリ・カスタムドメイン
- 仮置きの数字には「(仮)」を付け、実測で置き換える

## 問い合わせ

情報システム担当(m_nakagawa@smilior.com)
