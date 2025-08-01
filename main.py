# -*- coding: utf-8 -*-
"""메인 실행 파일"""

import tkinter as tk
from gui import ImageToIcoGUI

def main():
    print("아이콘 변환기 시작")
    print("=" * 40)
    
    root = tk.Tk()
    app = ImageToIcoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
