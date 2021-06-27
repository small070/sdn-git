import os
import time
import pyautogui


currentMouseX, currentMouseY = pyautogui.position()  # 鼠标当前位置
print(currentMouseX, currentMouseY)


for i in range(0, 920, 1):
    # 2535 305
    pyautogui.moveTo(2535, 305, duration=0.25)
    pyautogui.click(2535, 305, 2, 0.25, button='left')
    pyautogui.typewrite('sudo ryu-manager time_controller.py', interval=0.03) # 每次输入间隔0.25秒，输入Hello world!
    pyautogui.press('enter')  # 按下并松开（轻敲）回车键

    time.sleep(2)

    # 3285 305
    pyautogui.moveTo(3285, 305, duration=0.25)
    pyautogui.click(3285, 305, 2, 0.25, button='left')
    pyautogui.typewrite('sudo python3 myTopo2.py', interval=0.03) # 每次输入间隔0.25秒，输入Hello world!
    pyautogui.press('enter')  # 按下并松开（轻敲）回车键
    time.sleep(2)
    pyautogui.press('enter')  # 按下并松开（轻敲）回车键
    pyautogui.typewrite('pingall', interval=0.03) # 每次输入间隔0.25秒，输入Hello world!
    pyautogui.press('enter')  # 按下并松开（轻敲）回车键
    pyautogui.press('up')  # 按下并松开（轻敲）回车键
    pyautogui.press('enter')  # 按下并松开（轻敲）回车键
    pyautogui.press('up')  # 按下并松开（轻敲）回车键
    pyautogui.press('enter')  # 按下并松开（轻敲）回车键
    pyautogui.press('up')  # 按下并松开（轻敲）回车键
    pyautogui.press('enter')  # 按下并松开（轻敲）回车键
    pyautogui.press('up')  # 按下并松开（轻敲）回车键
    pyautogui.press('enter')  # 按下并松开（轻敲）回车键
    time.sleep(18)
    pyautogui.hotkey('ctrl', 'z') # 组合按键（Ctrl+V），粘贴功能，按下并松开'ctrl'和'v'按键
    # 3285 795
    pyautogui.moveTo(3285, 795, duration=0.25)
    pyautogui.click(3285, 795, 2, 0.25, button='left')
    pyautogui.typewrite('sudo mn -c', interval=0.03) # 每次输入间隔0.25秒，输入Hello world!
    pyautogui.press('enter')  # 按下并松开（轻敲）回车键
    pyautogui.typewrite('sudo killall -9 ryu-manager', interval=0.03)  # 每次输入间隔0.25秒，输入Hello world!
    pyautogui.press('enter')  # 按下并松开（轻敲）回车键
    time.sleep(5)
