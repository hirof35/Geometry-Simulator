import tkinter as tk
import math

class GeometrySimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("合同と相似シミュレーター")
        
        # 状態変数
        self.scale = 1.0       # 拡大率（相似用）
        self.angle = 0         # 回転角度（合同用）
        self.offset_x = 0      # 平行移動X
        self.offset_y = 0      # 平行移動Y
        
        # 基準となる三角形の頂点（ローカル座標）
        self.base_triangle = [(0, -50), (-60, 40), (60, 40)]
        
        self.create_widgets()
        self.draw_shapes()

    def create_widgets(self):
        # メインフレーム
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10) # 左右(padx)と上下(pady)の余白に修正
        
        # キャンバス（描画エリア）
        self.canvas = tk.Canvas(main_frame, width=600, height=400, bg="white")
        self.canvas.pack(side=tk.LEFT)
        
        # コントロールパネル
        control_frame = tk.LabelFrame(main_frame, text=" 操作パネル ")
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        # --- 合同変形（形と大きさを変えない） ---
        tk.Label(control_frame, text="【合同変形】", fg="blue", font=("", 10, "bold")).pack(anchor="w", pady=5)
        
        tk.Label(control_frame, text="平行移動 X:").pack(anchor="w")
        self.slider_x = tk.Scale(control_frame, from_=-150, to=150, orient=tk.HORIZONTAL, command=self.update_shapes)
        self.slider_x.pack(fill=tk.X)
        
        tk.Label(control_frame, text="平行移動 Y:").pack(anchor="w")
        self.slider_y = tk.Scale(control_frame, from_=-150, to=150, orient=tk.HORIZONTAL, command=self.update_shapes)
        self.slider_y.pack(fill=tk.X)
        
        tk.Label(control_frame, text="回転角度 (度):").pack(anchor="w")
        self.slider_angle = tk.Scale(control_frame, from_=0, to=360, orient=tk.HORIZONTAL, command=self.update_shapes)
        self.slider_angle.pack(fill=tk.X)
        
        # --- 相似変形（形は同じで大きさを変える） ---
        tk.Label(control_frame, text="【相似変形】", fg="green", font=("", 10, "bold")).pack(anchor="w", pady=10)
        
        tk.Label(control_frame, text="拡大・縮小倍率:").pack(anchor="w")
        self.slider_scale = tk.Scale(control_frame, from_=0.2, to=2.5, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_shapes)
        self.slider_scale.set(1.0)
        self.slider_scale.pack(fill=tk.X)
        
        # 説明ラベル
        info_text = (
            "赤：基準の図形\n"
            "青：合同な図形\n"
            "（位置や向きが変わっても合同）\n"
            "緑：相似な図形\n"
            "（大きさが変わっても相似）"
        )
        tk.Label(control_frame, text=info_text, justify=tk.LEFT, fg="gray").pack(anchor="w", pady=15)

    def transform_point(self, pt, scale, angle_deg, dx, dy):
        """頂点座標を拡大縮小、回転、平行移動させる関数"""
        x, y = pt
        # 1. 拡大縮小（相似）
        x *= scale
        y *= scale
        
        # 2. 回転（合同）
        rad = math.radians(angle_deg)
        rx = x * math.cos(rad) - y * math.sin(rad)
        ry = x * math.sin(rad) + y * math.cos(rad)
        
        # 3. 平行移動（合同）
        return rx + dx, ry + dy

    def update_shapes(self, _=None):
        # スライダーの値を取得
        self.offset_x = self.slider_x.get()
        self.offset_y = self.slider_y.get()
        self.angle = self.slider_angle.get()
        self.scale = self.slider_scale.get()
        
        self.draw_shapes()

    def draw_shapes(self):
        self.canvas.delete("all")
        
        # キャンバスの中心を基準点にする
        cx, cy = 300, 200
        
        # グリッド（背景の線）の描画
        for i in range(0, 600, 40):
            self.canvas.create_line(i, 0, i, 400, fill="#f0f0f0")
        for i in range(0, 400, 40):
            self.canvas.create_line(0, i, 600, i, fill="#f0f0f0")
            
        # 1. 基準の三角形（赤）
        ref_center_x, ref_center_y = cx - 130, cy
        ref_points = [(x + ref_center_x, y + ref_center_y) for x, y in self.base_triangle]
        self.canvas.create_polygon(ref_points, fill="", outline="red", width=3)
        self.canvas.create_text(ref_center_x, ref_center_y + 60, text="基準の三角形 A", fill="red", font=("", 10, "bold"))
        
        # 2. 合同な三角形（青）
        # 基準の三角形に対して「平行移動」と「回転」のみを行う（サイズは1.0倍固定）
        congruent_center_x, congruent_center_y = cx + 130, cy
        congruent_points = []
        for pt in self.base_triangle:
            tx, ty = self.transform_point(pt, scale=1.0, angle_deg=self.angle, dx=self.offset_x, dy=self.offset_y)
            congruent_points.append((tx + congruent_center_x, ty + congruent_center_y))
            
        self.canvas.create_polygon(congruent_points, fill="", outline="blue", width=3, dash=(4, 2))
        self.canvas.create_text(congruent_center_x + self.offset_x, congruent_center_y + self.offset_y + 70, 
                                text=f"合同な三角形 B\n(回転: {self.angle}°)", fill="blue", justify=tk.CENTER)

        # 3. 相似な三角形（緑）
        # 基準の三角形に対して「拡大・縮小」を行う
        similar_points = []
        for pt in self.base_triangle:
            tx, ty = self.transform_point(pt, scale=self.scale, angle_deg=0, dx=0, dy=0)
            similar_points.append((tx + ref_center_x, ty + ref_center_y)) # 基準と同じ位置に重ねて変化を見せる
            
        self.canvas.create_polygon(similar_points, fill="", outline="green", width=2)
        self.canvas.create_text(ref_center_x, ref_center_y - 70, 
                                text=f"相似な三角形 C\n(倍率: {self.scale}倍)", fill="green", justify=tk.CENTER)

if __name__ == "__main__":
    root = tk.Tk()
    app = GeometrySimulator(root)
    root.mainloop()
