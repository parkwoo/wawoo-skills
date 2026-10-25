# skills-main 思想との整合（方針）

対象：`.kilo/`（skills 55・agents 21・commands 13）。

## 思想（skills-main 要約）
1. small / easy to adapt / composable
2. プロセスを所有するフレームワークを避ける（GSD/BMAD/Spec-Kit）
3. curated
4. harness 固有を skill に入れない（設定は `AGENTS.md`／fork）
5. 編集可能コピー
6. model-invoked / user-invoked の明示
7. 既存で合成できるなら新規 skill を作らない

## 本キットの立場（意図的なハイブリッド）
- **プロセスは workflows（commands）が所有**し、skills-main の思考法・解法を各ステップに埋め込む。
- **skills＝参照知**、**agents＝役割**。
- skills-main の「フレームワーク回避」は**採らない**（プロセス制御を優先）。**コンテンツ（思考法）は採る**。
- 理由：agent が skill を飛ばす前提で、**workflow が明示的に呼ぶ**方が信頼できる。

## トレードオフ
- フレームワークの保守コストは増える → workflow は**薄く**保ち、skill の更新を容易にする。
- 「小さく合成」は **workflow のステップ設計**で活かす。
