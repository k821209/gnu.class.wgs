#!/usr/bin/env python3
"""
Script to extract individual slides from the main WGS_Class1_Presentation.html file
and create separate HTML files for each slide.
"""

import re
import os

def extract_slides(input_file, output_dir):
    """Extract slides from the main presentation file"""
    
    # Read the main presentation file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the CSS styles from the head section
    css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    css_styles = css_match.group(1) if css_match else ""
    
    # Fix the CSS for individual slides - make slides visible by default
    css_styles = css_styles.replace(
        '.slide { width: 100%; height: 100vh; display: none;',
        '.slide { width: 100%; height: 100vh; display: block;'
    )
    
    # Find all slide sections
    slide_pattern = r'<!-- Slide (\d+): (.*?) -->\s*<div class="slide[^"]*">(.*?)</div>\s*(?=<!-- Slide|\s*<div class="navigation">|$)'
    slides = re.findall(slide_pattern, content, re.DOTALL)
    
    print(f"Found {len(slides)} slides")
    
    slide_titles = [
        "Title Page",
        "Learning Objectives", 
        "NGS Technology Overview",
        "Sanger Sequencing Detail",
        "Sanger Technology Advantages",
        "Illumina NGS Technology",
        "MGI Sequencing Technology", 
        "Long-read Overview",
        "PacBio SMRT Technology",
        "Oxford Nanopore Technology",
        "Long-read Applications",
        "NGS Library Preparation",
        "Sanger vs NGS Comparison",
        "Platform Comparison",
        "WGS Data Characteristics",
        "Coverage and Read Depth",
        "Sequencing Errors",
        "Real Data Examples",
        "FastQC Report Analysis",
        "Quality Assessment Guidelines",
        "Summary"
    ]
    
    # Create individual slide files
    for i, (slide_num, slide_title_comment, slide_content) in enumerate(slides):
        slide_number = i + 1
        slide_title = slide_titles[i] if i < len(slide_titles) else f"Slide {slide_number}"
        
        # Fix image paths for slides subdirectory
        slide_content = slide_content.replace('./data/', 'data/')
        slide_content = slide_content.replace('../data/', 'data/')
        
        # Create the HTML template for this slide
        html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WGS 기초 이론 - {slide_title}</title>
    <style>
{css_styles}
    </style>
</head>
<body>

<div class="slide">
{slide_content.strip()}
</div>

<div class="navigation">
    <button class="jump-btn" onclick="jumpToFirst()">🏠 처음</button>
    <button class="nav-btn" onclick="prevSlide()"{'disabled' if slide_number == 1 else ''}>◀ 이전</button>
    <button class="nav-btn" onclick="nextSlide()"{'disabled' if slide_number == 21 else ''}>다음 ▶</button>
    <button class="fullscreen-btn" onclick="toggleFullscreen()">⛶ 전체화면</button>
</div>

<div class="slide-number">슬라이드 {slide_number} / 21</div>

<script>
    function prevSlide() {{
        {f'window.location.href = "slide{slide_number-1:02d}.html";' if slide_number > 1 else 'return false;'}
    }}
    
    function nextSlide() {{
        {f'window.location.href = "slide{slide_number+1:02d}.html";' if slide_number < 21 else 'return false;'}
    }}
    
    function jumpToFirst() {{
        {'window.location.href = "slide01.html";' if slide_number > 1 else 'return false;'}
    }}
    
    function toggleFullscreen() {{
        if (!document.fullscreenElement) {{
            document.documentElement.requestFullscreen();
        }} else {{
            if (document.exitFullscreen) {{
                document.exitFullscreen();
            }}
        }}
    }}
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {{
        if (e.key === 'ArrowRight' || e.key === ' ') {{
            nextSlide();
        }} else if (e.key === 'ArrowLeft') {{
            prevSlide();
        }} else if (e.key === 'Home') {{
            jumpToFirst();
        }} else if (e.key === 'F11') {{
            e.preventDefault();
            toggleFullscreen();
        }}
    }});
</script>

</body>
</html>"""

        # Write the slide file
        output_file = os.path.join(output_dir, f"slide{slide_number:02d}.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print(f"Created: {output_file} - {slide_title}")

if __name__ == "__main__":
    input_file = "../WGS_Class1_Presentation.html"
    output_dir = "."
    
    if os.path.exists(input_file):
        extract_slides(input_file, output_dir)
        print(f"\nAll slides extracted successfully!")
        print(f"Open index.html to view the slide navigation")
    else:
        print(f"Input file {input_file} not found!")