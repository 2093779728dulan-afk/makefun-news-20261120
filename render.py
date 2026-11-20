#!/usr/bin/env python3
"""
Render a newspaper front page for November 20, 2026 world news.
Output: assets/entry.png (1024x1024, PNG, <=1MB)
"""

from PIL import Image, ImageDraw, ImageFont
import os

WIDTH = 1024
HEIGHT = 1024
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "assets", "entry.png")

def get_font(size, bold=False, italic=False):
    try:
        if bold and italic:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf", size)
        elif bold:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        elif italic:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", size)
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def draw_text_wrapped(draw, text, x, y, font, max_width, fill="black", line_spacing=3):
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    
    for i, line in enumerate(lines):
        draw.text((x, y + i * (font.size + line_spacing)), line, font=font, fill=fill)
    
    return len(lines) * (font.size + line_spacing)

def draw_column_headline(draw, x, y, width, kicker, headline, font_kicker, font_headline, fill_kicker, fill_headline, line_color):
    """Draw a two-line column headline with kicker and main headline"""
    draw.text((x, y), kicker, font=font_kicker, fill=fill_kicker)
    kicker_h = font_kicker.size + 4
    draw.text((x, y + kicker_h), headline, font=font_headline, fill=fill_headline)
    headline_h = font_headline.size + 4
    draw.line([(x, y + kicker_h + headline_h + 4), (x + width, y + kicker_h + headline_h + 4)], fill=line_color, width=1)
    return kicker_h + headline_h + 12

def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), color="#f5f0e1")
    draw = ImageDraw.Draw(img)
    
    # Fonts - slightly larger for better legibility
    font_title = get_font(44, bold=True)
    font_date = get_font(17)
    font_headline_main = get_font(30, bold=True)
    font_subhead_main = get_font(25, bold=True)
    font_quote = get_font(21, bold=True, italic=True)
    font_kicker = get_font(15, bold=True)
    font_col_headline = get_font(18, bold=True)
    font_body = get_font(16)
    font_body_sm = get_font(15)
    font_byline = get_font(11)
    font_caption = get_font(13, bold=True)
    font_small = get_font(13)
    font_tiny = get_font(10)
    
    # Colors - more newspaper-authentic
    BLACK = "#1a1a1a"
    DARK_GRAY = "#2d2d2d"
    MED_GRAY = "#4a4a4a"
    RED = "#b30000"
    BLUE = "#002b5c"
    LINE_COLOR = "#b0b0b0"
    RULE_COLOR = "#888888"
    ACCENT_BG = "#fff8e7"
    
    y = 18
    
    # Masthead - with decorative rules
    draw.rectangle([0, y, WIDTH, y + 82], fill=BLACK)
    draw.text((40, y + 10), "THE DAILY CHRONICLE", font=font_title, fill="white")
    draw.text((40, y + 56), "Est. 1884  |  VOL. CXLII  |  NO. 324  |  $2.00", font=font_date, fill="#cccccc")
    # Thin decorative rules under masthead
    draw.line([(40, y + 82), (WIDTH - 40, y + 82)], fill=RED, width=2)
    draw.line([(40, y + 85), (WIDTH - 40, y + 85)], fill=LINE_COLOR, width=1)
    y += 100
    
    # Date line
    draw.line([(40, y), (WIDTH - 40, y)], fill=RULE_COLOR, width=2)
    y += 12
    draw.text((40, y), "FRIDAY, NOVEMBER 20, 2026", font=font_caption, fill=BLACK)
    draw.text((WIDTH - 200, y), "WORLD EDITION", font=font_caption, fill=BLUE)
    y += 30
    draw.line([(40, y), (WIDTH - 40, y)], fill=RULE_COLOR, width=1)
    y += 22
    
    # Main headline area (top story - Trilateral Summit)
    # Full-width box with subtle accent background
    main_box_h = 185
    draw.rectangle([38, y, WIDTH - 38, y + main_box_h], fill=ACCENT_BG, outline=BLACK, width=2)
    draw.line([(38, y + 2), (WIDTH - 38, y + 2)], fill=RED, width=3)  # Red top rule
    
    x_main = 58
    y_main = y + 18
    draw.text((x_main, y_main), "HISTORIC FIRST TRILATERAL SUMMIT", font=font_headline_main, fill=RED)
    draw.text((x_main, y_main + 42), "Trump, Xi and Putin Meet in Shenzhen, Issue \"Peace Declaration\"", font=font_subhead_main, fill=BLACK)
    draw.text((x_main, y_main + 82), "\"A nuclear war cannot be won and must never be fought\"", font=font_quote, fill=BLUE)
    draw_text_wrapped(draw, "Three leaders pledge denuclearization framework, Ukraine ceasefire, Taiwan dialogue", x_main, y_main + 115, font_body, WIDTH - 140, fill=MED_GRAY)
    draw.text((x_main, y_main + 145), "By JAMES CHEN, Chief Diplomatic Correspondent", font=font_byline, fill=MED_GRAY)
    
    # Bottom rule on main box
    draw.line([(58, y + main_box_h - 20), (WIDTH - 58, y + main_box_h - 20)], fill=LINE_COLOR, width=1)
    y += main_box_h + 18
    
    # Four columns below
    col_width = (WIDTH - 110) // 4
    col_gap = 15
    col_starts = [40 + i * (col_width + col_gap) for i in range(4)]
    row_y = y
    col_height = 315
    
    # Column 1: ICJ Myanmar ruling
    x = col_starts[0]
    draw.rectangle([x, row_y, x + col_width, row_y + col_height], fill="white", outline=LINE_COLOR, width=1)
    draw.line([(x, row_y), (x + col_width, row_y)], fill=RED, width=3)
    h_used = draw_column_headline(draw, x + 10, row_y + 8, col_width - 20,
        "WORLD", "ICJ Rules Myanmar Committed Genocide", font_kicker, font_col_headline, RED, BLACK, LINE_COLOR)
    body1 = "The International Court of Justice has ruled that Myanmar committed genocide against the Rohingya Muslim minority, marking the first time the UN's top court has held a state responsible for the crime of genocide. The 15-judge panel found Myanmar's 2017 military campaign constituted genocidal acts."
    draw_text_wrapped(draw, body1, x + 10, row_y + 8 + h_used, font_body_sm, col_width - 20, fill=DARK_GRAY, line_spacing=2)
    draw.text((x + 10, row_y + col_height - 22), "By MARIA SANTOS, The Hague", font=font_byline, fill=MED_GRAY)
    
    # Column 2: Anthropic IPO
    x = col_starts[1]
    draw.rectangle([x, row_y, x + col_width, row_y + col_height], fill="white", outline=LINE_COLOR, width=1)
    draw.line([(x, row_y), (x + col_width, row_y)], fill=RED, width=3)
    h_used = draw_column_headline(draw, x + 10, row_y + 8, col_width - 20,
        "TECHNOLOGY", "Anthropic's Record IPO Largest Ever at $107B", font_kicker, font_col_headline, RED, BLACK, LINE_COLOR)
    body2 = "Anthropic shattered records with a $107 billion IPO at a $1.5 trillion valuation, the largest public offering ever. Shares surged 42% on debut as investors bet on constitutional AI leadership. The raise dwarfs Saudi Aramco's $29.4B record."
    draw_text_wrapped(draw, body2, x + 10, row_y + 8 + h_used, font_body_sm, col_width - 20, fill=DARK_GRAY, line_spacing=2)
    draw.text((x + 10, row_y + col_height - 22), "By DAVID PARK, Tech Editor", font=font_byline, fill=MED_GRAY)
    
    # Column 3: US Midterms
    x = col_starts[2]
    draw.rectangle([x, row_y, x + col_width, row_y + col_height], fill="white", outline=LINE_COLOR, width=1)
    draw.line([(x, row_y), (x + col_width, row_y)], fill=RED, width=3)
    h_used = draw_column_headline(draw, x + 10, row_y + 8, col_width - 20,
        "POLITICS", "Democrats Sweep Midterms, Biggest House Win in 50 Years", font_kicker, font_col_headline, RED, BLACK, LINE_COLOR)
    body3 = "Democrats captured 56% of the House vote vs 42% for Republicans, the largest margin since 1974. Hakeem Jeffries nominated for Speaker. Gains driven by abortion rights, democracy concerns, and economic anxiety. Senate remains 51-49 Democratic."
    draw_text_wrapped(draw, body3, x + 10, row_y + 8 + h_used, font_body_sm, col_width - 20, fill=DARK_GRAY, line_spacing=2)
    draw.text((x + 10, row_y + col_height - 22), "By SARAH WILLIAMS, Washington", font=font_byline, fill=MED_GRAY)
    
    # Column 4: US-Venezuela military ties
    x = col_starts[3]
    draw.rectangle([x, row_y, x + col_width, row_y + col_height], fill="white", outline=LINE_COLOR, width=1)
    draw.line([(x, row_y), (x + col_width, row_y)], fill=RED, width=3)
    h_used = draw_column_headline(draw, x + 10, row_y + 8, col_width - 20,
        "DEFENSE", "U.S.-Venezuela Restore Military Ties", font_kicker, font_col_headline, RED, BLACK, LINE_COLOR)
    body4 = "Defense Secretary Pete Hegseth made a surprise visit to Caracas, signing a defense cooperation agreement restoring military-to-military contacts severed since 2019. Pact includes counter-narcotics, disaster response, and regional security coordination."
    draw_text_wrapped(draw, body4, x + 10, row_y + 8 + h_used, font_body_sm, col_width - 20, fill=DARK_GRAY, line_spacing=2)
    draw.text((x + 10, row_y + col_height - 22), "By CARLOS MENDOZA, Caracas", font=font_byline, fill=MED_GRAY)
    
    y = row_y + col_height + 18
    
    # Bottom section - additional stories with better styling
    draw.line([(40, y), (WIDTH - 40, y)], fill=RULE_COLOR, width=2)
    draw.line([(40, y + 3), (WIDTH - 40, y + 3)], fill=LINE_COLOR, width=1)
    y += 18
    
    draw.text((50, y), "ALSO IN TODAY'S EDITION", font=font_caption, fill=BLACK)
    y += 28
    
    stories = [
        ("Climate Summit Opens in Baku", "COP32 delegates confront 1.5°C gap as emissions hit record highs"),
        ("China's GDP Growth Beats Forecasts", "4.8% Q3 expansion eases deflation fears, yuan strengthens"),
        ("Bird Flu Spreads to US Dairy Herds", "CDC raises alert level; vaccine stockpile activated nationwide"),
        ("EU Passes AI Liability Directive", "First comprehensive framework for AI harm accountability"),
    ]
    
    bot_col_w = (WIDTH - 110) // 2
    for i, (headline, sub) in enumerate(stories):
        col = i % 2
        row = i // 2
        sx = 50 + col * (bot_col_w + 10)
        sy = y + row * 65
        # Bullet with accent color
        draw.text((sx, sy), "▸", font=font_caption, fill=RED)
        draw.text((sx + 15, sy), headline, font=get_font(14, bold=True), fill=BLACK)
        draw_text_wrapped(draw, sub, sx + 15, sy + 22, font_small, bot_col_w - 15, fill=MED_GRAY, line_spacing=1)
    
    y += 145
    
    # Footer with weather/market summary box on left
    draw.line([(40, y), (WIDTH - 40, y)], fill=RULE_COLOR, width=1)
    y += 12
    
    # Small market/weather box
    box_x = 40
    box_w = 280
    box_h = 55
    draw.rectangle([box_x, y, box_x + box_w, y + box_h], fill=ACCENT_BG, outline=LINE_COLOR, width=1)
    draw.text((box_x + 8, y + 4), "MARKETS  (close Nov 19)", font=font_tiny, fill=BLUE)
    draw.text((box_x + 8, y + 18), "Dow 42,350  ▼0.3%   S&P 5,890  ▼0.2%   Nasdaq 18,720  ▼0.4%", font=font_tiny, fill=DARK_GRAY)
    draw.text((box_x + 8, y + 32), "Oil $72.40/bbl  ▼1.1%   Gold $2,680  ▲0.2%   Bitcoin $98,400  ▼2.1%", font=font_tiny, fill=DARK_GRAY)
    draw.text((box_x + 8, y + 44), "Weather NYC: 52°/38°  ☁  London: 48°/41°  🌧  Singapore: 86°/78°  ⛈", font=font_tiny, fill=DARK_GRAY)
    
    # Copyright
    draw.text((WIDTH - 300, y + 10), "© 2026 The Daily Chronicle", font=font_tiny, fill=MED_GRAY)
    draw.text((WIDTH - 300, y + 22), "All rights reserved", font=font_tiny, fill=MED_GRAY)
    draw.text((WIDTH - 300, y + 34), "www.dailychronicle.example", font=font_tiny, fill=MED_GRAY)
    draw.text((WIDTH - 300, y + 46), "Printed in New York, London, Singapore", font=font_tiny, fill=MED_GRAY)
    
    # Save
    img.save(OUTPUT_PATH, "PNG", optimize=True, compress_level=9)
    size = os.path.getsize(OUTPUT_PATH)
    print(f"Saved to {OUTPUT_PATH}")
    print(f"Size: {size} bytes ({size/1024:.1f} KB)")
    
    # Verify dimensions
    with Image.open(OUTPUT_PATH) as im:
        print(f"Dimensions: {im.size}")

if __name__ == "__main__":
    main()