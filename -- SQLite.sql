-- SQLite
-- 商品テーブル（在庫管理の基本単位）
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,           -- 例: g, ml, 個など
    current_stock REAL NOT NULL DEFAULT 0,  -- 現在の在庫数
    alert_threshold REAL DEFAULT 0         -- 発注アラートの閾値
);

-- 在庫の入出庫履歴
CREATE TABLE stock_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    movement_type TEXT CHECK(movement_type IN ('in', 'out')) NOT NULL,
    quantity REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    note TEXT,
    FOREIGN KEY (item_id) REFERENCES items(id)
);

-- 売上データ（販売数に応じて在庫を減らす）
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    quantity_sold REAL NOT NULL,
    sale_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id)
);
