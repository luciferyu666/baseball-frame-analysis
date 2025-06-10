# ⚾️ 棒球逐幀分析系統（Baseball Frame Analysis）— 端到端系統

此專案是一個模組化、容器化的端到端系統，專為棒球領域的**逐幀影片分析**而設計，包含物件偵測（YOLOv8）、姿勢估測（MediaPipe）、光學字元辨識（OCR）、事件整合、資料庫儲存（TimescaleDB）與即時 REST API（FastAPI）。

## 🗂️ 專案結構

```
.
├─ docker/            # 容器建置檔案與 Docker Compose 堆疊
├─ src/               # 核心原始碼（模組化分層架構）
├─ data/              # 原始影片、處理後影格、輸出資料、模型權重
├─ mlruns/            # MLflow 實驗追蹤資料
├─ notebooks/         # 探索性分析與視覺化 Jupyter Notebooks
└─ tests/             # 單元測試與整合測試套件
```

## 🚀 快速開始

```bash
# 1. 複製專案並進入目錄
git clone <repo-url> && cd baseball-frame-analysis

# 2. 建置並啟動服務（GPU 環境）
docker compose -f docker/docker-compose.yml up -d --build

# 3. 使用範例影片執行分析流程
python -m src run_pipeline --video data/raw/sample.mp4 --out data/outputs
```

完整的使用指南（包含模型訓練流程、資料庫儀表板與 API 文件），請參閱：

`/docs/architecture.md`

## 🛠️ 環境設定

將 `.env.example` 複製為 `.env` 並設定以下參數：

```env
DATABASE_URI=postgresql+asyncpg://postgres:postgres@db:5432/baseball
MLFLOW_TRACKING_URI=file:///workspace/mlruns
CUDA_VISIBLE_DEVICES=0
```

## 📄 授權條款

本專案以 MIT 授權條款釋出。詳情請參考 `LICENSE` 檔案。
