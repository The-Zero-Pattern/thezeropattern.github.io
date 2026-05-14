from PIL import Image, ImageDraw, ImageFilter

def generate_recaman_sequence(steps):
    seq = [0]
    seen = {0}
    for i in range(1, steps):
        prev = seq[-1]
        next_val = prev - i
        if next_val > 0 and next_val not in seen:
            seq.append(next_val)
            seen.add(next_val)
        else:
            next_val = prev + i
            seq.append(next_val)
            seen.add(next_val)
    return seq

def calculate_bounds(seq, canvas_size, padding):
    min_x = min(seq)
    max_x = max(seq)
    
    max_radius = 0
    for i in range(len(seq) - 1):
        radius = abs(seq[i] - seq[i+1]) / 2.0
        if radius > max_radius:
            max_radius = radius
            
    seq_width = max_x - min_x
    seq_height = max_radius * 2
    
    available_size = canvas_size - (padding * 2)
    scale_x = available_size / seq_width if seq_width > 0 else 1
    scale_y = available_size / seq_height if seq_height > 0 else 1
    
    scale = min(scale_x, scale_y)
    used_width = seq_width * scale
    used_height = seq_height * scale
    
    offset_x = padding + (available_size - used_width) / 2
    offset_y = padding + (available_size - used_height) / 2 + (max_radius * scale)
    
    return scale, offset_x, offset_y

def draw_sequence(draw, seq, scale, offset_x, offset_y, color, line_width):
    for i in range(len(seq) - 1):
        start = seq[i]
        end = seq[i + 1]
        
        left = min(start, end) * scale + offset_x
        right = max(start, end) * scale + offset_x
        radius = (right - left) / 2.0
        
        bbox = [left, offset_y - radius, right, offset_y + radius]
        
        if i % 2 == 0:
            draw.arc(bbox, 180, 360, fill=color, width=line_width)
        else:
            draw.arc(bbox, 0, 180, fill=color, width=line_width)

def generate_favicon():
    print("Generating favicon.ico...")
    size = 128
    padding = 8
    
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    seq = generate_recaman_sequence(15)
    scale, offset_x, offset_y = calculate_bounds(seq, size, padding)
    
    draw_sequence(draw, seq, scale, offset_x, offset_y, (0, 212, 255, 255), 6)
    
    favicon = img.resize((32, 32), Image.Resampling.LANCZOS)
    favicon.save("favicon.ico", format="ICO")
    print("favicon.ico saved.")

def generate_high_res_logo():
    print("Generating High-Res logo.png...")
    size = 1024
    padding = 100
    
    img = Image.new("RGBA", (size, size), (15, 23, 42, 255))
    seq = generate_recaman_sequence(25)
    scale, offset_x, offset_y = calculate_bounds(seq, size, padding)
    
    glow_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    draw_sequence(glow_draw, seq, scale, offset_x, offset_y, (0, 212, 255, 180), 24)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(15))
    
    img.alpha_composite(glow_layer)
    
    core_draw = ImageDraw.Draw(img)
    draw_sequence(core_draw, seq, scale, offset_x, offset_y, (241, 245, 249, 255), 6)
    
    img.save("recaman-logo.png")
    print("recaman-logo.png saved.")

if __name__ == "__main__":
    generate_favicon()
    generate_high_res_logo()
