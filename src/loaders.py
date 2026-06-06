import pandas as pd
from src.interfaces import IDataLoader

class DummyDataLoader(IDataLoader):
    def load(self) -> pd.DataFrame:
        data = {
            'LotNo':       ["Lot1", "Lot2", "Lot3", "Lot4"], # Lot4が異常ロット
            'total_chips': [1000,   1000,   1000,   1000],   # 各ロットの総チップ数
            'defect1_count': [10,     15,     12,     250],   # Lot4で異常スパイク（気泡不良など）
            'defect2_count': [5,      30,      6,      7],    # Lot2で異常スパイク（キズ不良など）
            'defect3_count': [2,      1,      3,      2],     # 常に平和な不良
            
            # --- 設備A（オーブン系パラメータ） ---
            'factor1':      [180.0,  182.0,  179.0,  230.0],  # ★defect1の真因（Lot4で跳ね上がり）
            'factor2':      [60.0,   61.0,   59.0,   60.0],   # 無関係（オーブン風量）
            'factor3':      [5.0,    5.2,    4.8,    5.1],    # 無関係（オーブン排気圧）
            
            # --- 設備B（ディスペンサー系パラメータ） ---
            'factor4':      [10.0,   35.0,   10.2,   9.8],    # ★defect2の真因（Lot2で跳ね上がり）
            'factor5':      [0.50,   0.51,   0.49,   0.50],   # 無関係（ノズルギャップ）
            'factor6':      [20.0,   22.0,   21.0,   20.5],   # 無関係（シリンジ残量）
            
            # --- 設備C・環境（その他パラメータ） ---
            'factor7':      [25.1,   26.3,   24.8,   25.5],   # 無関係（クリーンルーム室温）
            'factor8':      [50.0,   52.0,   48.0,   51.0],   # 無関係（クリーンルーム湿度）
            'factor9':      [120.0,  121.0,  119.0,  120.5],  # 無関係（コンベア搬送速度）
        }
        return pd.DataFrame(data)


class FileDataLoader(IDataLoader):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path)
