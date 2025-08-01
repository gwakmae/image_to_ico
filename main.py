# -*- coding: utf-8 -*-
"""메인 실행 파일"""

import tkinter as tk
from gui import ImageToIcoGUI
import sys # sys 모듈 추가
import io  # io 모듈 추가

def main():
    # 콘솔 출력 인코딩을 UTF-8로 설정 (추가된 부분)
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

    print("아이콘 변환기 시작")
    print("=" * 40)
    
    root = tk.Tk()
    app = ImageToIcoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()