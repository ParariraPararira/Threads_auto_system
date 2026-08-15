# Threads自動投稿システム - セットアップ手順

このシステムは、GitHubのウェブサイト画面だけで設定できます。
ターミナルやCodespacesを開く必要はありません。

## ステップ1：ファイルをアップロードする

1. GitHubで `Threads_auto_system` リポジトリを開く
2. 「Add file」→「Upload files」を選択
3. このフォルダの中身をすべてドラッグ＆ドロップ
4. 「Commit changes」で保存

## ステップ2：GitHub Pages を有効にする（認証コード受け取り用ページ）

1. リポジトリの「Settings」タブを開く
2. 左メニューの「Pages」を選択
3. 「Source」を `Deploy from a branch` にし、ブランチを `main`、フォルダを `/docs` に設定して保存
4. 少し待つと、`https://ユーザー名.github.io/Threads_auto_system/` のようなURLが発行される
   → これが「THREADS_REDIRECT_URI」になります

## ステップ3：Metaアプリ側にリダイレクトURIを登録する

1. developers.facebook.com の「Threads自動投稿」アプリを開く
2. 「Threads API にアクセス」→「設定」で、ステップ2で発行されたURLを
   「有効なOAuthリダイレクトURI」に追加して保存

## ステップ4：Secrets（機密情報）を登録する

1. リポジトリの「Settings」→「Secrets and variables」→「Actions」を開く
2. 「New repository secret」で、以下を1つずつ登録する

| Name | 値 |
|---|---|
| THREADS_APP_ID | Threadsアプリ ID（例: 1963109741321787） |
| THREADS_APP_SECRET | Threadsのapp secret |
| THREADS_REDIRECT_URI | ステップ2で発行されたURL |

（THREADS_USER_ID と THREADS_ACCESS_TOKEN は、ステップ6で自動取得できるので今は登録不要です）

## ステップ5：認証コードを取得する

1. 以下のURLを組み立ててブラウザで開く（{APP_ID}と{REDIRECT_URI}は自分の値に置き換え）
   ```
   https://threads.net/oauth/authorize?client_id={APP_ID}&redirect_uri={REDIRECT_URI}&scope=threads_basic,threads_content_publish&response_type=code
   ```
2. Threadsアカウントでログインし、許可する
3. ステップ2で作ったページに転送され、認証コードが表示される
4. 「コピー」ボタンでコピーする

## ステップ6：長期アクセストークンを取得する（ボタン操作のみ）

1. リポジトリの「Actions」タブを開く
2. 左メニューから「Threadsトークン取得」を選ぶ
3. 「Run workflow」ボタンを押す
4. 入力欄に、ステップ5でコピーした認証コードを貼り付けて実行
5. 実行が終わったら、そのログ（緑のチェックマークの行）を開き、
   表示された「THREADS_ACCESS_TOKEN」と「THREADS_USER_ID」の値をコピー
6. ステップ4の手順で、この2つをそれぞれSecretsに登録する

## ステップ7：動作確認

1. 「Actions」タブ →「毎日のThreads投稿」を選ぶ
2. 「Run workflow」で手動実行し、実際にThreadsに投稿されるか確認する
3. 成功すると `logs/post_log.csv` に記録が残る

## 以降の自動実行

一度ここまで設定すれば、毎日決まった時刻（現在は日本時間9時）に
自動で投稿されるようになります。何も操作は不要です。

## 今後の拡張予定

- GPT・Gemini・Claudeによる投稿文の自動生成
- LINE公式アカウントへの投稿前確認通知
- note記事の下書き自動生成、流入・売上の記録
