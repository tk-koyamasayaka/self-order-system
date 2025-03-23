FROM node:16-alpine

WORKDIR /app

# 依存関係のインストール
COPY package*.json ./
RUN npm install

# アプリケーションのコードをコピー
COPY . .

# ポートを公開
EXPOSE 8080

# コンテナ起動時のコマンド
CMD ["npm", "run", "serve"]