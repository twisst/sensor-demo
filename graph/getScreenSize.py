
def screenSize(horizontal,vertical):
    # Screen size in pixels
    screen_width_pixels = horizontal
    screen_height_pixels = vertical

    # Assume a standard DPI value (adjust if needed)
    standard_dpi = 100

    # Convert screen size from pixels to inches
    screen_width_inches = screen_width_pixels / standard_dpi
    screen_height_inches = screen_height_pixels / standard_dpi

    # Print the converted values
    print("Screen size in inches:")
    print(f"Width: {screen_width_inches} inches")
    print(f"Height: {screen_height_inches} inches")

    return (screen_width_inches, screen_height_inches)
