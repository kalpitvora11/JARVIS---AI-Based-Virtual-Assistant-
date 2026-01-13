import screen_brightness_control as sbc


current_brightness = sbc.get_brightness()
print(current_brightness)
a = int(input("Enter the brightness level:"))
controlled_brightness=sbc.set_brightness(a)