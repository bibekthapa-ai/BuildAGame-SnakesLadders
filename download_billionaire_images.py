#!/usr/bin/env python3
"""
Helper script to download billionaire images for the game
"""
import os
import sys

def main():
    """Main function to provide instructions for downloading billionaire images"""
    print("Billionaire Snakes and Ladders - Image Download Helper")
    print("=====================================================")
    print("\nTo complete the game setup, you need to download images of billionaires.")
    print("Please download the following images and save them in the 'assets/images' folder:")
    
    # Create assets directory if it doesn't exist
    if not os.path.exists("assets/images"):
        os.makedirs("assets/images")
        print("\nCreated 'assets/images' directory.")
    
    # Create sounds directory if it doesn't exist
    if not os.path.exists("assets/sounds"):
        os.makedirs("assets/sounds")
        print("Created 'assets/sounds' directory.")
    
    # List of billionaires and their image filenames
    billionaires = [
        ("Elon Musk", "elon_musk.png"),
        ("Jeff Bezos", "jeff_bezos.png"),
        ("Bernard Arnault", "bernard_arnault.png"),
        ("Mark Zuckerberg", "mark_zuckerberg.png"),
        ("Bill Gates", "bill_gates.png"),
        ("Warren Buffett", "warren_buffett.png"),
        ("Larry Ellison", "larry_ellison.png"),
        ("Larry Page", "larry_page.png"),
        ("Sergey Brin", "sergey_brin.png"),
        ("Steve Ballmer", "steve_ballmer.png"),
        ("Mukesh Ambani", "mukesh_ambani.png"),
        ("Jensen Huang", "jensen_huang.png"),
        ("Michael Bloomberg", "michael_bloomberg.png"),
        ("Carlos Slim Helu", "carlos_slim_helu.png"),
        ("Francoise Bettencourt Meyers", "francoise_bettencourt_meyers.png")
    ]
    
    print("\nBillionaire images needed:")
    for i, (name, filename) in enumerate(billionaires, 1):
        print(f"{i}. {name} -> {filename}")
    
    print("\nAdditional images needed:")
    print("1. Ladder image -> ladder.png")
    print("2. Dice images -> dice_1.png, dice_2.png, dice_3.png, dice_4.png, dice_5.png, dice_6.png")
    
    print("\nSound files needed (in assets/sounds):")
    print("1. Dice roll sound -> dice_roll.wav")
    print("2. Movement sound -> move.wav")
    print("3. Snake sound -> snake.wav")
    print("4. Ladder sound -> ladder.wav")
    print("5. Win sound -> win.wav")
    
    print("\nNote: The game will still work with placeholder graphics if you don't provide these files.")
    print("You can find free sound effects on websites like freesound.org.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
