# 環境構築（サンプル対戦時）
python3 -m venv ssvenv

source ssvenv/bin/activate

pip install -U ./game

pip install -U ./client

※./gameでゲーム本体が、./clientでサンプルプレイヤーがインストールされる
ゲーム本体：blocks_duo_ss
サンプルプレイヤー：ss_tarou

# サンプルプレイヤーでの実行
start_blocksduo ss_tarou ss_tarou

💡発表資料は[こちら](https://docs.google.com/presentation/d/1Gk4SO-4Fz3hwd9SK5HQSCKoQrS_5lqbb3UjWP_nTBmY/edit?hl=JA#slide=id.g2e024a97e2c_0_0)
