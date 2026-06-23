"""
giai_tay_lbp.py
Script trich xuat ma tran pixel va giai tay LBP tung buoc.
Chay: python giai_tay_lbp.py
"""
import os, sys, math
import numpy as np
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')

# ─────────────────────────────────────────────
# CẤU HÌNH – Thay đổi theo yêu cầu
# ─────────────────────────────────────────────
ANH        = os.path.join("anh_xlas", "anh_xlas", "image_01.jpg")  # Đường dẫn ảnh
PIXEL_Y    = 100    # Hàng của pixel trung tâm (cy)
PIXEL_X    = 100    # Cột của pixel trung tâm (cx)
P          = 8      # Số điểm lân cận
R          = 1      # Bán kính
# ─────────────────────────────────────────────

W = "\033[0m"       # Reset
B = "\033[1m"       # Bold
YEL= "\033[93m"     # Vàng
CYN= "\033[96m"     # Cyan
GRN= "\033[92m"     # Xanh lá
RED= "\033[91m"     # Đỏ
MAG= "\033[95m"     # Tím

def noi_suy_song_tuyen(anh, y, x):
    rows, cols = anh.shape
    x0 = int(math.floor(x)); x1 = x0 + 1
    y0 = int(math.floor(y)); y1 = y0 + 1
    x0 = max(0,min(x0,cols-1)); x1 = max(0,min(x1,cols-1))
    y0 = max(0,min(y0,rows-1)); y1 = max(0,min(y1,rows-1))
    dx = x - math.floor(x)
    dy = y - math.floor(y)
    f00=anh[y0,x0]; f01=anh[y0,x1]; f10=anh[y1,x0]; f11=anh[y1,x1]
    gp=(1-dy)*(1-dx)*f00+(1-dy)*dx*f01+dy*(1-dx)*f10+dy*dx*f11
    return gp, x0, x1, y0, y1, dx, dy, f00, f01, f10, f11

def print_matrix(anh_xam, cy, cx, half=4):
    """In ma trận pixel xung quanh (cy, cx)."""
    rows, cols = anh_xam.shape
    size = 2*half + 1
    print(f"\n{'═'*70}")
    print(f"{B}{CYN}  MA TRẬN PIXEL {size}×{size} XUNG QUANH PIXEL TRUNG TÂM ({cy},{cx}){W}")
    print(f"{'═'*70}")

    # Header cột
    print("       ", end="")
    for c in range(cx-half, cx+half+1):
        cc = max(0, min(c, cols-1))
        label = f"c={cc:3d}" if c == cx else f"c={cc:3d}"
        print(f"{label:7s}", end="")
    print()
    print("       " + "─"*((size)*7))

    for r in range(cy-half, cy+half+1):
        rr = max(0, min(r, rows-1))
        label = f"r={rr:3d}│"
        print(label, end="")
        for c in range(cx-half, cx+half+1):
            cc = max(0, min(c, cols-1))
            val = int(anh_xam[rr, cc])
            if r == cy and c == cx:
                print(f"{YEL}{B}{val:6d}{W} ", end="")   # Pixel tâm - vàng
            elif abs(r-cy) <= R and abs(c-cx) <= R:
                print(f"{CYN}{val:6d}{W} ", end="")       # Vùng R - cyan
            else:
                print(f"{val:6d} ", end="")
        print()

    print(f"\n  {YEL}■{W} = Pixel trung tâm (gc={int(anh_xam[cy,cx])})")
    print(f"  {CYN}■{W} = Vùng lân cận R={R}")

def print_neighbor_ring(anh_xam, cy, cx):
    """In vòng tròn 3×3 cho P=8, R=1 (minh họa thứ tự lân cận)."""
    if P == 8 and R == 1:
        rows, cols = anh_xam.shape
        print(f"\n{'─'*50}")
        print(f"{B}  Thứ tự 8 điểm lân cận (P=8, R=1){W}")
        print(f"{'─'*50}")
        # Tính tọa độ và giá trị 8 lân cận
        neighbors = []
        for p in range(P):
            angle = 2*math.pi*p/P
            xp = cx + R*math.cos(angle)
            yp = cy - R*math.sin(angle)
            gp, *_ = noi_suy_song_tuyen(anh_xam, yp, xp)
            neighbors.append((p, round(xp,2), round(yp,2), round(gp,1)))

        # In lưới 3×3 dạng bảng
        gc = int(anh_xam[cy, cx])
        # Ánh xạ p → vị trí trong lưới 3×3
        # Góc 0° = phải (p=0), ngược chiều kim đồng hồ khi hình học
        # Sau reverse: p=0 ở trên-trái (do code gốc reverse)
        offsets_disp = [
            (-1,-1), (-1, 0), (-1,+1),
            ( 0,-1),           ( 0,+1),
            (+1,-1), (+1, 0), (+1,+1),
        ]
        # Vị trí p trong lưới (tính theo góc thực)
        angle_to_grid = {}
        for p, xp, yp, gp in neighbors:
            dr = round(yp - cy); dc = round(xp - cx)
            angle_to_grid[(dr,dc)] = (p, int(round(gp)))

        print(f"  ┌─────────┬─────────┬─────────┐")
        for row_off in [-1, 0, 1]:
            print(f"  │", end="")
            for col_off in [-1, 0, 1]:
                if row_off == 0 and col_off == 0:
                    print(f" {YEL}{B}gc={gc:3d}{W}  │", end="")
                elif (row_off, col_off) in angle_to_grid:
                    p_idx, gp_v = angle_to_grid[(row_off, col_off)]
                    bit = 1 if gp_v >= gc else 0
                    col = GRN if bit else RED
                    print(f" {col}p{p_idx}={gp_v:3d}{W} │", end="")
                else:
                    print(f"    ?    │", end="")
            print()
            if row_off < 1:
                print(f"  ├─────────┼─────────┼─────────┤")
        print(f"  └─────────┴─────────┴─────────┘")
        print(f"\n  {GRN}■{W} bit=1 (gp ≥ gc)   {RED}■{W} bit=0 (gp < gc)   {YEL}■{W} tâm (gc)")

def print_step_by_step(anh_xam, cy, cx):
    """In từng bước tính LBP chi tiết."""
    gc = anh_xam[cy, cx]
    print(f"\n{'═'*70}")
    print(f"{B}{MAG}  GIẢI TAY TỪNG BƯỚC – LBP (P={P}, R={R}){W}")
    print(f"{'═'*70}")
    print(f"\n{B}  Bước 1: Lấy mức sáng pixel trung tâm{W}")
    print(f"  gc = anh_xam[{cy}, {cx}] = {YEL}{B}{int(gc)}{W}")
    print(f"\n{B}  Bước 2: Tính từng điểm lân cận{W}")
    print(f"  {'p':>3} │ {'Góc (°)':>8} │ {'xp':>8} │ {'yp':>8} │ {'gp':>8} │ {'gc':>6} │ {'So sánh':>10} │ {'bit':>4}")
    print(f"  {'─'*3}─┼─{'─'*8}─┼─{'─'*8}─┼─{'─'*8}─┼─{'─'*8}─┼─{'─'*6}─┼─{'─'*10}─┼─{'─'*4}")

    bits = []
    for p in range(P):
        angle = 2*math.pi*p/P
        angle_deg = angle * 180 / math.pi
        xp = cx + R*math.cos(angle)
        yp = cy - R*math.sin(angle)
        gp, x0,x1,y0,y1,dx,dy,f00,f01,f10,f11 = noi_suy_song_tuyen(anh_xam, yp, xp)
        gp_r = round(gp, 1)
        bit = 1 if gp_r >= gc else 0
        bits.append(bit)
        cmp = f"gp≥gc ✓" if bit else f"gp<gc ✗"
        bit_col = GRN if bit else RED
        print(f"  {p:>3} │ {angle_deg:>8.1f} │ {xp:>8.3f} │ {yp:>8.3f} │ {gp_r:>8.1f} │ {int(gc):>6} │ {cmp:>10} │ {bit_col}{bit:>4}{W}")

    print(f"\n{B}  Bước 3: Chuỗi bit nhị phân{W}")
    bit_str = "".join(str(b) for b in bits)
    print(f"  bits = [{', '.join(str(b) for b in bits)}]")
    print(f"  chuỗi = {CYN}{bit_str}{W}")

    print(f"\n{B}  Bước 4: Chia nhóm 8-bit → thập phân{W}")
    so_nhom = P // 8
    group_vals = []
    for g in range(so_nhom):
        nhom = bits[g*8:(g+1)*8]
        val = sum(b*(2**i) for i,b in enumerate(nhom))
        group_vals.append(val)
        terms = " + ".join(f"{b}×2^{i}={b*(2**i)}" for i,b in enumerate(nhom) if b)
        if not terms: terms = "0"
        print(f"  Nhóm {g+1}: [{', '.join(str(b) for b in nhom)}]")
        print(f"         = {terms} = {GRN}{B}{val}{W}")

    max_val = max(group_vals)
    print(f"\n{B}  Bước 5: Lấy MAX → Giá trị LBP{W}")
    if so_nhom > 1:
        print(f"  max({', '.join(str(v) for v in group_vals)}) = {YEL}{B}{max_val}{W}")
    print(f"\n  ╔══════════════════════════════╗")
    print(f"  ║  LBP({cy},{cx}) = {YEL}{B}{max_val:>3}{W}             ║")
    print(f"  ╚══════════════════════════════╝")

    return max_val

def print_bilinear_detail(anh_xam, cy, cx, p_idx=0):
    """In chi tiết nội suy song tuyến cho 1 điểm lân cận."""
    gc = anh_xam[cy, cx]
    angle = 2*math.pi*p_idx/P
    xp = cx + R*math.cos(angle)
    yp = cy - R*math.sin(angle)
    gp, x0,x1,y0,y1,dx,dy,f00,f01,f10,f11 = noi_suy_song_tuyen(anh_xam, yp, xp)

    print(f"\n{'─'*60}")
    print(f"{B}  Chi tiết Nội suy song tuyến – Điểm lân cận p={p_idx}{W}")
    print(f"{'─'*60}")
    print(f"  Góc    = 2π × {p_idx}/{P} = {angle:.4f} rad = {angle*180/math.pi:.1f}°")
    print(f"  xp     = {cx} + {R} × cos({angle:.4f}) = {xp:.4f}")
    print(f"  yp     = {cy} − {R} × sin({angle:.4f}) = {yp:.4f}")
    print(f"\n  Tọa độ nguyên:")
    print(f"  x0={x0}, x1={x1}, y0={y0}, y1={y1}")
    print(f"  dx = {xp:.4f} − {x0} = {dx:.4f}")
    print(f"  dy = {yp:.4f} − {y0} = {dy:.4f}")
    print(f"\n  4 pixel góc gần nhất:")
    print(f"  f00=anh[{y0},{x0}]={int(f00)}   f01=anh[{y0},{x1}]={int(f01)}")
    print(f"  f10=anh[{y1},{x0}]={int(f10)}   f11=anh[{y1},{x1}]={int(f11)}")
    print(f"\n  Công thức nội suy song tuyến:")
    print(f"  gp = (1−{dy:.3f})(1−{dx:.3f})×{int(f00)}")
    print(f"     + (1−{dy:.3f})×{dx:.3f}×{int(f01)}")
    print(f"     + {dy:.3f}×(1−{dx:.3f})×{int(f10)}")
    print(f"     + {dy:.3f}×{dx:.3f}×{int(f11)}")
    t1=(1-dy)*(1-dx)*f00; t2=(1-dy)*dx*f01; t3=dy*(1-dx)*f10; t4=dy*dx*f11
    print(f"     = {t1:.2f} + {t2:.2f} + {t3:.2f} + {t4:.2f}")
    print(f"  gp = {CYN}{B}{round(gp,2)}{W}")
    bit = 1 if round(gp,1) >= gc else 0
    print(f"\n  So sánh: gp={round(gp,2)} {'≥' if bit else '<'} gc={int(gc)} → bit = {GRN if bit else RED}{B}{bit}{W}")

def export_for_teacher(anh_xam, cy, cx, max_val):
    """In bản tóm tắt sạch để chép tay."""
    gc = anh_xam[cy, cx]
    half = max(2, R+1)
    bits = []
    for p in range(P):
        angle = 2*math.pi*p/P
        xp = cx + R*math.cos(angle)
        yp = cy - R*math.sin(angle)
        gp, *_ = noi_suy_song_tuyen(anh_xam, yp, xp)
        bits.append(1 if round(gp,1) >= gc else 0)

    print(f"\n{'═'*70}")
    print(f"{B}  BẢN TÓM TẮT – DÙNG ĐỂ VIẾT TAY CHO THẦY{W}")
    print(f"{'═'*70}")
    print(f"\n  Ảnh: {ANH}")
    print(f"  Pixel trung tâm: ({cy}, {cx})")
    print(f"  Cấu hình: P={P}, R={R}")
    print(f"\n  ┌ Ma trận lân cận ({2*half+1}×{2*half+1}): ┐")
    rows, cols = anh_xam.shape
    for r in range(cy-half, cy+half+1):
        print(f"  │  ", end="")
        for c in range(cx-half, cx+half+1):
            rr=max(0,min(r,rows-1)); cc=max(0,min(c,cols-1))
            v=int(anh_xam[rr,cc])
            if r==cy and c==cx:
                print(f"[{YEL}{v:3d}{W}]", end=" ")
            else:
                print(f" {v:3d} ", end=" ")
        print("│")
    print(f"  └──────────────────────────────────────────────────┘")
    print(f"\n  gc (tâm) = {YEL}{B}{int(gc)}{W}")
    print(f"  Chuỗi {P} bit: {CYN}{''.join(str(b) for b in bits)}{W}")
    so_nhom = P // 8
    group_vals = []
    for g in range(so_nhom):
        nhom = bits[g*8:(g+1)*8]
        val = sum(b*(2**i) for i,b in enumerate(nhom))
        group_vals.append(val)
        print(f"  Nhóm {g+1}: {nhom} = {GRN}{val}{W}")
    print(f"  MAX({', '.join(str(v) for v in group_vals)}) = {YEL}{B}{max_val}{W}")
    print(f"\n  ► LBP({cy},{cx}) = {YEL}{B}{max_val}{W}")
    print(f"{'═'*70}\n")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print(f"\n{B}{MAG}{'═'*70}")
    print(f"  GIẢI TAY LBP – TRÍCH XUẤT MA TRẬN VÀ TÍNH TỪNG BƯỚC")
    print(f"{'═'*70}{W}")

    # Đọc ảnh
    if not os.path.exists(ANH):
        print(f"{RED}  ❌ Không tìm thấy ảnh: {ANH}{W}")
        return
    img = Image.open(ANH).convert('L')
    anh_xam = np.array(img, dtype=np.float64)
    H, W2 = anh_xam.shape
    print(f"\n  Ảnh: {ANH}  ({H}×{W2} pixels)")
    print(f"  Pixel chọn: ({PIXEL_Y}, {PIXEL_X})")
    print(f"  Cấu hình: P={P}, R={R}")

    cy, cx = PIXEL_Y, PIXEL_X
    if not (0 <= cy < H and 0 <= cx < W2):
        print(f"{RED}  ❌ Tọa độ ({cy},{cx}) ngoài ảnh ({H}×{W2}){W}")
        return

    # In ma trận
    print_matrix(anh_xam, cy, cx, half=4)

    # In vòng tròn 3×3 (nếu P=8, R=1)
    if P == 8 and R == 1:
        print_neighbor_ring(anh_xam, cy, cx)

    # In từng bước
    max_val = print_step_by_step(anh_xam, cy, cx)

    # In chi tiết nội suy cho điểm lân cận đầu tiên
    print(f"\n{B}  Muốn xem chi tiết nội suy cho điểm lân cận nào? (0-{P-1}, Enter=bỏ qua):{W} ", end="")
    try:
        inp = input().strip()
        if inp.isdigit() and 0 <= int(inp) < P:
            print_bilinear_detail(anh_xam, cy, cx, int(inp))
    except:
        pass

    # In bản tóm tắt
    export_for_teacher(anh_xam, cy, cx, max_val)

if __name__ == "__main__":
    main()
