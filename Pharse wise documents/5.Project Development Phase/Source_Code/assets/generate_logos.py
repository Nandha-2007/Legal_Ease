"""Generate brand logos for LegalEase (logo.png and inverseLogo.png)."""
from PIL import Image, ImageDraw, ImageFont
import os

def draw_scales_icon(draw, center_x, center_y, scale=1.0, color=(30, 41, 59, 255)):
    # Draw scales of justice
    w = int(24 * scale)
    h = int(32 * scale)
    
    # Top beam
    beam_w = int(20 * scale)
    beam_y = center_y - int(8 * scale)
    draw.line([(center_x - beam_w, beam_y), (center_x + beam_w, beam_y)], fill=color, width=max(2, int(2.5 * scale)))
    
    # Center pillar
    draw.line([(center_x, center_y - int(14 * scale)), (center_x, center_y + int(14 * scale))], fill=color, width=max(2, int(3 * scale)))
    
    # Base
    base_w = int(12 * scale)
    draw.line([(center_x - base_w, center_y + int(14 * scale)), (center_x + base_w, center_y + int(14 * scale))], fill=color, width=max(2, int(3.5 * scale)))
    
    # Top finial / circle
    draw.ellipse([(center_x - int(3 * scale), center_y - int(17 * scale)), (center_x + int(3 * scale), center_y - int(11 * scale))], fill=color)
    
    # Left pan strings & pan
    left_x = center_x - beam_w
    pan_drop = int(12 * scale)
    pan_w = int(9 * scale)
    pan_y = beam_y + pan_drop
    draw.line([(left_x, beam_y), (left_x - pan_w, pan_y)], fill=color, width=max(1, int(1.5 * scale)))
    draw.line([(left_x, beam_y), (left_x + pan_w, pan_y)], fill=color, width=max(1, int(1.5 * scale)))
    # pan bowl
    draw.arc([(left_x - pan_w, pan_y - int(3*scale)), (left_x + pan_w, pan_y + int(5*scale))], start=0, end=180, fill=color, width=max(2, int(2 * scale)))
    
    # Right pan strings & pan
    right_x = center_x + beam_w
    draw.line([(right_x, beam_y), (right_x - pan_w, pan_y)], fill=color, width=max(1, int(1.5 * scale)))
    draw.line([(right_x, beam_y), (right_x + pan_w, pan_y)], fill=color, width=max(1, int(1.5 * scale)))
    # pan bowl
    draw.arc([(right_x - pan_w, pan_y - int(3*scale)), (right_x + pan_w, pan_y + int(5*scale))], start=0, end=180, fill=color, width=max(2, int(2 * scale)))

def create_logo(filename, is_dark_mode=False):
    width, height = 480, 120
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if is_dark_mode:
        icon_color = (255, 255, 255, 240)
        text_color = (248, 250, 252, 255)
        sub_color = (148, 163, 184, 255)
    else:
        icon_color = (20, 30, 48, 255)
        text_color = (15, 23, 42, 255)
        sub_color = (71, 85, 105, 255)
        
    # Draw scales icon
    draw_scales_icon(draw, center_x=60, center_y=60, scale=2.0, color=icon_color)
    
    # Try system fonts, fallback to default
    font_main = None
    font_sub = None
    for font_path in ["arialbd.ttf", "calibrib.ttf", "segoeuib.ttf", "timesbd.ttf"]:
        try:
            font_main = ImageFont.truetype(font_path, 44)
            font_sub = ImageFont.truetype(font_path.replace("bd", "").replace("b", ""), 14)
            break
        except Exception:
            continue
            
    if font_main is None:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    draw.text((120, 26), "LegalEase", font=font_main, fill=text_color)
    draw.text((122, 74), "AI-POWERED LEGAL DOCUMENT GENERATOR", font=font_sub, fill=sub_color)
    
    out_dir = os.path.join(os.path.dirname(__file__), "logo")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)
    img.save(out_path, format="PNG")
    print(f"Generated logo at: {out_path}")

if __name__ == "__main__":
    create_logo("logo.png", is_dark_mode=False)
    create_logo("inverseLogo.png", is_dark_mode=True)
