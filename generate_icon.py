#!/usr/bin/env python3
"""Generate a simple clock icon in comic style"""

from PIL import Image, ImageDraw, ImageFont
import math

# Create a new image with a colorful background
size = 512
img = Image.new('RGBA', (size, size), (255, 255, 255, 0))  # Transparent background
draw = ImageDraw.Draw(img)

# Draw a colorful circle as background (light blue)
circle_color = (70, 130, 180, 255)  # Steel blue
draw.ellipse([20, 20, size-20, size-20], fill=circle_color, outline=(40, 80, 140, 255), width=8)

# Draw a white circle for the clock face
clock_color = (255, 255, 255, 255)
clock_margin = 80
draw.ellipse([clock_margin, clock_margin, size-clock_margin, size-clock_margin], fill=clock_color, outline=(0, 0, 0, 255), width=6)

# Draw clock numbers (12, 3, 6, 9)
center_x, center_y = size // 2, size // 2
radius = (size - 2*clock_margin) // 2 - 20

# Function to draw a number at a given hour position
def draw_number(hour, text):
    angle = math.radians(90 - hour * 30)  # Convert hour to angle (12 is at top)
    x = center_x + radius * 0.75 * math.cos(angle)
    y = center_y - radius * 0.75 * math.sin(angle)
    
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Draw text centered
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw.text((x - text_width//2, y - text_height//2), text, fill=(0, 0, 0, 255), font=font)

# Draw 12, 3, 6, 9
draw_number(12, "12")
draw_number(3, "3")
draw_number(6, "6")
draw_number(9, "9")

# Draw hour hand (pointing to 10)
hour_angle = math.radians(90 - 10 * 30)
hour_length = radius * 0.5
hour_x = center_x + hour_length * math.cos(hour_angle)
hour_y = center_y - hour_length * math.sin(hour_angle)
draw.line([(center_x, center_y), (hour_x, hour_y)], fill=(0, 0, 0, 255), width=8)

# Draw minute hand (pointing to 2)
minute_angle = math.radians(90 - 2 * 6)  # 2 minutes = 12 degrees
minute_length = radius * 0.65
minute_x = center_x + minute_length * math.cos(minute_angle)
minute_y = center_y - minute_length * math.sin(minute_angle)
draw.line([(center_x, center_y), (minute_x, minute_y)], fill=(255, 0, 0, 255), width=6)

# Draw center dot
dot_radius = 12
draw.ellipse([center_x-dot_radius, center_y-dot_radius, center_x+dot_radius, center_y+dot_radius], fill=(0, 0, 0, 255))

# Add a little comic-style "pow" effect at the edge
# Draw a small star-burst
burst_x, burst_y = size - 60, 60
for i in range(8):
    angle = math.radians(i * 45)
    x_end = burst_x + 40 * math.cos(angle)
    y_end = burst_y + 40 * math.sin(angle)
    draw.line([(burst_x, burst_y), (x_end, y_end)], fill=(255, 200, 0, 255), width=4)

# Save the icon
output_path = "c:\\Users\\Bene\\Desktop\\Python_Programme\\icon.png"
img.save(output_path, 'PNG')
print(f"Icon saved to {output_path}")
