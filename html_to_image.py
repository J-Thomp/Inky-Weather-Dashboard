#!/usr/bin/env python3
"""
Convert rendered HTML to PNG image
Requires: pip install html2image
"""

try:
    from html2image import Html2Image
    import os

    print("Converting HTML to image...")

    # Create Html2Image instance
    hti = Html2Image(output_path='.', size=(800, 480))

    # Convert the rendered HTML file to PNG
    hti.screenshot(
        html_file='weather_rendered.html',
        css_file='weather.css',
        save_as='weather_dashboard.png'
    )

    print("[OK] Image saved as: weather_dashboard.png")
    print("\nYou can now view weather_dashboard.png to see your dashboard!")

except ImportError:
    print("ERROR: html2image not installed")
    print("\nPlease install it with:")
    print("  pip install html2image")
    print("\nNote: html2image requires Chrome or Chromium to be installed")
except Exception as e:
    print(f"Error: {e}")
    print("\nAlternative: Open weather_rendered.html in a browser and take a screenshot!")
