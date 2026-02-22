#!/usr/bin/env python3
"""
Generate minimal placeholder PNG images for the Ren'Py GUI system.
Pure Python - no external dependencies (uses zlib and struct only).
"""

import struct
import zlib
import os

BASE = "/home/user/Visual-Novel-Test/game/gui"


def make_png(width, height, pixels_func):
    """
    Create a PNG file in memory. pixels_func(x, y) returns (r, g, b, a).
    Returns bytes of the complete PNG file.
    """
    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack('>I', len(data)) + c + crc

    # PNG signature
    sig = b'\x89PNG\r\n\x1a\n'

    # IHDR: width, height, bit depth 8, color type 6 (RGBA)
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr = chunk(b'IHDR', ihdr_data)

    # IDAT: image data
    raw_rows = []
    for y in range(height):
        row = b'\x00'  # filter byte: None
        for x in range(width):
            r, g, b, a = pixels_func(x, y)
            row += struct.pack('BBBB', r, g, b, a)
        raw_rows.append(row)
    raw_data = b''.join(raw_rows)
    compressed = zlib.compress(raw_data, 9)
    idat = chunk(b'IDAT', compressed)

    # IEND
    iend = chunk(b'IEND', b'')

    return sig + ihdr + idat + iend


def solid_color(r, g, b, a):
    """Return a pixel function that always returns the same color."""
    def func(x, y):
        return (r, g, b, a)
    return func


def save_png(path, width, height, pixels_func):
    """Generate and save a PNG file."""
    data = make_png(width, height, pixels_func)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)
    size_kb = len(data) / 1024
    print(f"  Created: {path}  ({width}x{height}, {size_kb:.1f} KB)")


def main():
    # --- 1. textbox.png: 1920x278, semi-transparent dark ---
    print("Generating GUI placeholder PNGs...")

    save_png(f"{BASE}/textbox.png", 1920, 278,
             solid_color(20, 20, 30, 200))

    # --- 2. namebox.png: 400x60 ---
    save_png(f"{BASE}/namebox.png", 400, 60,
             solid_color(20, 20, 30, 200))

    # --- 3. frame.png: 100x100 ---
    save_png(f"{BASE}/frame.png", 100, 100,
             solid_color(25, 25, 35, 210))

    # --- 4. nvl.png: 1920x1080 ---
    save_png(f"{BASE}/nvl.png", 1920, 1080,
             solid_color(15, 15, 25, 220))

    # --- 5. skip.png: 200x40 ---
    save_png(f"{BASE}/skip.png", 200, 40,
             solid_color(20, 20, 30, 200))

    # --- 6. notify.png: 600x50 ---
    save_png(f"{BASE}/notify.png", 600, 50,
             solid_color(20, 20, 30, 200))

    # --- 7. overlay/main_menu.png: 420x1080, gradient dark overlay ---
    def main_menu_overlay(x, y):
        # Horizontal gradient: fully opaque dark on left, fading to transparent on right
        if x < 300:
            a = 220
        else:
            t = (x - 300) / 120.0
            t = min(1.0, max(0.0, t))
            a = int(220 * (1.0 - t))
        return (15, 15, 25, a)

    save_png(f"{BASE}/overlay/main_menu.png", 420, 1080,
             main_menu_overlay)

    # --- 8. overlay/game_menu.png: 1920x1080 ---
    save_png(f"{BASE}/overlay/game_menu.png", 1920, 1080,
             solid_color(15, 15, 25, 180))

    # --- 9. overlay/confirm.png: 1920x1080 ---
    save_png(f"{BASE}/overlay/confirm.png", 1920, 1080,
             solid_color(15, 15, 25, 200))

    # --- 10-13. Radio buttons (30x30) ---
    def radio_idle(x, y):
        cx, cy, r = 15, 15, 12
        dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        if abs(dist - r) < 1.8:
            return (180, 180, 180, 255)
        return (0, 0, 0, 0)

    def radio_hover(x, y):
        cx, cy, r = 15, 15, 12
        dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        if abs(dist - r) < 1.8:
            return (255, 255, 255, 255)
        return (0, 0, 0, 0)

    def radio_selected_idle(x, y):
        cx, cy = 15, 15
        r_outer, r_inner = 12, 6
        dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        if abs(dist - r_outer) < 1.8:
            return (180, 180, 180, 255)
        if dist <= r_inner + 0.5:
            return (180, 180, 180, 255)
        return (0, 0, 0, 0)

    def radio_selected_hover(x, y):
        cx, cy = 15, 15
        r_outer, r_inner = 12, 6
        dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        if abs(dist - r_outer) < 1.8:
            return (255, 255, 255, 255)
        if dist <= r_inner + 0.5:
            return (255, 255, 255, 255)
        return (0, 0, 0, 0)

    save_png(f"{BASE}/button/radio_idle_foreground.png", 30, 30, radio_idle)
    save_png(f"{BASE}/button/radio_hover_foreground.png", 30, 30, radio_hover)
    save_png(f"{BASE}/button/radio_selected_idle_foreground.png", 30, 30, radio_selected_idle)
    save_png(f"{BASE}/button/radio_selected_hover_foreground.png", 30, 30, radio_selected_hover)

    # --- 14-17. Checkboxes (30x30) ---
    def check_idle(x, y):
        # Square outline
        border = 2
        if (x < border or x >= 30 - border or y < border or y >= 30 - border):
            if 1 <= x <= 28 and 1 <= y <= 28:
                return (180, 180, 180, 255)
        return (0, 0, 0, 0)

    def check_hover(x, y):
        border = 2
        if (x < border or x >= 30 - border or y < border or y >= 30 - border):
            if 1 <= x <= 28 and 1 <= y <= 28:
                return (255, 255, 255, 255)
        return (0, 0, 0, 0)

    def check_selected_idle(x, y):
        # Square outline + checkmark (diagonal lines)
        border = 2
        is_border = False
        if (x < border or x >= 30 - border or y < border or y >= 30 - border):
            if 1 <= x <= 28 and 1 <= y <= 28:
                is_border = True

        # Simple checkmark: two line segments
        # Segment 1: (6,15) to (12,22)
        # Segment 2: (12,22) to (24,8)
        is_check = False
        if 6 <= x <= 12:
            expected_y = 15 + (x - 6) * 7.0 / 6.0
            if abs(y - expected_y) < 2.0:
                is_check = True
        if 12 <= x <= 24:
            expected_y = 22 - (x - 12) * 14.0 / 12.0
            if abs(y - expected_y) < 2.0:
                is_check = True

        if is_border or is_check:
            return (180, 180, 180, 255)
        return (0, 0, 0, 0)

    def check_selected_hover(x, y):
        border = 2
        is_border = False
        if (x < border or x >= 30 - border or y < border or y >= 30 - border):
            if 1 <= x <= 28 and 1 <= y <= 28:
                is_border = True

        is_check = False
        if 6 <= x <= 12:
            expected_y = 15 + (x - 6) * 7.0 / 6.0
            if abs(y - expected_y) < 2.0:
                is_check = True
        if 12 <= x <= 24:
            expected_y = 22 - (x - 12) * 14.0 / 12.0
            if abs(y - expected_y) < 2.0:
                is_check = True

        if is_border or is_check:
            return (255, 255, 255, 255)
        return (0, 0, 0, 0)

    save_png(f"{BASE}/button/check_idle_foreground.png", 30, 30, check_idle)
    save_png(f"{BASE}/button/check_hover_foreground.png", 30, 30, check_hover)
    save_png(f"{BASE}/button/check_selected_idle_foreground.png", 30, 30, check_selected_idle)
    save_png(f"{BASE}/button/check_selected_hover_foreground.png", 30, 30, check_selected_hover)

    # --- main_menu.png: 1920x1080 dark background ---
    save_png(f"{BASE}/main_menu.png", 1920, 1080,
             solid_color(25, 20, 35, 255))

    # --- game_menu.png: 1920x1080 dark background ---
    save_png(f"{BASE}/game_menu.png", 1920, 1080,
             solid_color(25, 20, 35, 255))

    # --- Bar images (gui/bar/) ---
    # Accent color (#6b4c8a) = rgb(107, 76, 138) for filled portion
    # Muted color (#3a3a5c) = rgb(58, 58, 92) for empty portion
    bar_h = 38  # gui.bar_size

    # left.png: filled portion of horizontal bar (accent color)
    save_png(f"{BASE}/bar/left.png", bar_h, bar_h,
             solid_color(107, 76, 138, 255))

    # right.png: empty portion of horizontal bar (muted color)
    save_png(f"{BASE}/bar/right.png", bar_h, bar_h,
             solid_color(58, 58, 92, 255))

    # top.png: filled portion of vertical bar (accent color)
    save_png(f"{BASE}/bar/top.png", bar_h, bar_h,
             solid_color(107, 76, 138, 255))

    # bottom.png: empty portion of vertical bar (muted color)
    save_png(f"{BASE}/bar/bottom.png", bar_h, bar_h,
             solid_color(58, 58, 92, 255))

    # --- Scrollbar images (gui/scrollbar/) ---
    sb_size = 18  # gui.scrollbar_size

    # Horizontal scrollbar
    save_png(f"{BASE}/scrollbar/horizontal_idle_bar.png", sb_size, sb_size,
             solid_color(58, 58, 92, 255))
    save_png(f"{BASE}/scrollbar/horizontal_hover_bar.png", sb_size, sb_size,
             solid_color(74, 74, 108, 255))
    save_png(f"{BASE}/scrollbar/horizontal_idle_thumb.png", sb_size, sb_size,
             solid_color(107, 76, 138, 255))
    save_png(f"{BASE}/scrollbar/horizontal_hover_thumb.png", sb_size, sb_size,
             solid_color(192, 160, 224, 255))

    # Vertical scrollbar
    save_png(f"{BASE}/scrollbar/vertical_idle_bar.png", sb_size, sb_size,
             solid_color(58, 58, 92, 255))
    save_png(f"{BASE}/scrollbar/vertical_hover_bar.png", sb_size, sb_size,
             solid_color(74, 74, 108, 255))
    save_png(f"{BASE}/scrollbar/vertical_idle_thumb.png", sb_size, sb_size,
             solid_color(107, 76, 138, 255))
    save_png(f"{BASE}/scrollbar/vertical_hover_thumb.png", sb_size, sb_size,
             solid_color(192, 160, 224, 255))

    # --- Slider images (gui/slider/) ---
    # Slider bars: same as scrollbar but at bar_size height
    save_png(f"{BASE}/slider/horizontal_idle_bar.png", bar_h, bar_h,
             solid_color(58, 58, 92, 255))
    save_png(f"{BASE}/slider/horizontal_hover_bar.png", bar_h, bar_h,
             solid_color(74, 74, 108, 255))

    # Slider thumbs: circular-ish thumb
    def slider_thumb_idle(x, y):
        cx, cy, r = bar_h // 2, bar_h // 2, bar_h // 2 - 2
        dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        if dist <= r:
            return (107, 76, 138, 255)
        return (0, 0, 0, 0)

    def slider_thumb_hover(x, y):
        cx, cy, r = bar_h // 2, bar_h // 2, bar_h // 2 - 2
        dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        if dist <= r:
            return (192, 160, 224, 255)
        return (0, 0, 0, 0)

    save_png(f"{BASE}/slider/horizontal_idle_thumb.png", bar_h, bar_h,
             slider_thumb_idle)
    save_png(f"{BASE}/slider/horizontal_hover_thumb.png", bar_h, bar_h,
             slider_thumb_hover)

    # Vertical slider
    save_png(f"{BASE}/slider/vertical_idle_bar.png", bar_h, bar_h,
             solid_color(58, 58, 92, 255))
    save_png(f"{BASE}/slider/vertical_hover_bar.png", bar_h, bar_h,
             solid_color(74, 74, 108, 255))
    save_png(f"{BASE}/slider/vertical_idle_thumb.png", bar_h, bar_h,
             slider_thumb_idle)
    save_png(f"{BASE}/slider/vertical_hover_thumb.png", bar_h, bar_h,
             slider_thumb_hover)

    print("\nAll GUI placeholder PNGs generated successfully!")


if __name__ == '__main__':
    main()
