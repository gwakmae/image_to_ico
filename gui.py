# -*- coding: utf-8 -*-
"""GUI 인터페이스"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
from config import *
from converter import ImageConverter

class ImageToIcoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("간단한 아이콘 변환기")
        self.root.geometry("600x500")
        
        self.converter = ImageConverter()
        self.selected_files = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 파일 선택
        file_frame = ttk.LabelFrame(main_frame, text="파일 선택", padding="5")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(file_frame, text="이미지 파일 선택", 
                  command=self.select_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_frame, text="초기화", 
                  command=self.clear_files).pack(side=tk.LEFT)
        
        # 파일 리스트
        list_frame = ttk.LabelFrame(main_frame, text="선택된 파일", padding="5")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.file_listbox = tk.Listbox(list_frame, height=6)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 간단한 설정
        settings_frame = ttk.LabelFrame(main_frame, text="설정", padding="5")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 자동 여백 제거
        self.auto_crop_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="자동 여백 제거", 
                       variable=self.auto_crop_var).pack(anchor=tk.W)
        
        # 크기 선택
        size_frame = ttk.Frame(settings_frame)
        size_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(size_frame, text="아이콘 크기:").pack(anchor=tk.W)
        
        sizes_frame = ttk.Frame(size_frame)
        sizes_frame.pack(anchor=tk.W, padx=(20, 0))
        
        self.size_vars = {}
        for i, size in enumerate(ICO_SIZES):
            var = tk.BooleanVar(value=size in DEFAULT_SETTINGS['selected_sizes'])
            self.size_vars[size] = var
            ttk.Checkbutton(sizes_frame, text=f"{size}px", variable=var).grid(
                row=i//4, column=i%4, sticky=tk.W, padx=(0, 10))
        
        # 출력 폴더
        output_frame = ttk.Frame(settings_frame)
        output_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(output_frame, text="출력 폴더:").pack(anchor=tk.W)
        
        folder_frame = ttk.Frame(output_frame)
        folder_frame.pack(fill=tk.X, padx=(20, 0))
        
        self.output_path_var = tk.StringVar(value="원본 파일과 같은 폴더")
        ttk.Entry(folder_frame, textvariable=self.output_path_var, 
                 state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(folder_frame, text="선택", 
                  command=self.select_output_folder).pack(side=tk.RIGHT)
        
        # 변환 버튼
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(10, 0))
        
        self.convert_button = ttk.Button(button_frame, text="변환 시작", 
                                        command=self.start_conversion)
        self.convert_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_button = ttk.Button(button_frame, text="중단", 
                                       command=self.cancel_conversion, state='disabled')
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="종료", command=self.root.quit).pack(side=tk.LEFT)
        
        # 진행률
        self.progress_var = tk.StringVar(value="변환할 파일을 선택하세요")
        ttk.Label(main_frame, textvariable=self.progress_var).pack(pady=(10, 5))
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X)
    
    def get_file_types(self):
        """파일 타입 목록 생성"""
        all_extensions = []
        file_types = [("모든 이미지 파일", "")]
        
        for format_name, extensions in SUPPORTED_FORMATS.items():
            ext_list = extensions.split(';')
            all_extensions.extend(ext_list)
            file_types.append((f"{format_name} 파일", extensions))
        
        file_types[0] = ("모든 이미지 파일", ";".join(all_extensions))
        return file_types
    
    def select_files(self):
        """파일 선택"""
        files = filedialog.askopenfilenames(
            title="변환할 이미지 파일 선택",
            filetypes=self.get_file_types()
        )
        
        if files:
            self.selected_files = list(files)
            self.update_file_list()
    
    def clear_files(self):
        """파일 목록 초기화"""
        self.selected_files = []
        self.update_file_list()
    
    def update_file_list(self):
        """파일 목록 업데이트"""
        self.file_listbox.delete(0, tk.END)
        for file_path in self.selected_files:
            self.file_listbox.insert(tk.END, os.path.basename(file_path))
        
        if self.selected_files:
            self.progress_var.set(f"{len(self.selected_files)}개 파일 선택됨")
        else:
            self.progress_var.set("변환할 파일을 선택하세요")
    
    def select_output_folder(self):
        """출력 폴더 선택"""
        folder = filedialog.askdirectory(title="출력 폴더 선택")
        if folder:
            self.output_path_var.set(folder)
    
    def get_settings(self):
        """현재 설정 가져오기"""
        return {
            'auto_crop': self.auto_crop_var.get(),
            'crop_threshold': 15,
            'icon_scale': 90,
            'allow_upscale': True,
            'resample_method': 'LANCZOS',
            'background_mode': 'transparent',
            'selected_sizes': [size for size, var in self.size_vars.items() if var.get()]
        }
    
    def progress_callback(self, current, total, filename):
        """진행률 콜백"""
        progress = (current / total) * 100
        self.progress_bar.config(value=progress)
        self.progress_var.set(f"변환 중... ({current+1}/{total}) - {filename}")
    
    def conversion_worker(self):
        """변환 작업 스레드"""
        try:
            settings = self.get_settings()
            
            if not settings['selected_sizes']:
                self.root.after(0, lambda: messagebox.showerror("오류", "크기를 하나 이상 선택해주세요."))
                return
            
            output_dir = self.output_path_var.get()
            
            success_count, total_files = self.converter.convert_multiple(
                self.selected_files, output_dir, settings, self.progress_callback
            )
            
            # 완료 메시지
            if success_count > 0:
                self.root.after(0, lambda: self.progress_var.set(f"✅ 완료! {success_count}/{total_files}개 성공"))
                self.root.after(0, lambda: messagebox.showinfo("완료", f"{success_count}개 파일이 변환되었습니다."))
            else:
                self.root.after(0, lambda: messagebox.showerror("실패", "변환에 실패했습니다."))
        
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("오류", f"변환 중 오류: {str(e)}"))
        
        finally:
            self.root.after(0, lambda: self.convert_button.config(state='normal'))
            self.root.after(0, lambda: self.cancel_button.config(state='disabled'))
    
    def start_conversion(self):
        """변환 시작"""
        if not self.selected_files:
            messagebox.showerror("오류", "파일을 선택해주세요.")
            return
        
        self.convert_button.config(state='disabled')
        self.cancel_button.config(state='normal')
        self.progress_bar.config(value=0)
        
        # 백그라운드 스레드에서 변환
        thread = threading.Thread(target=self.conversion_worker, daemon=True)
        thread.start()
    
    def cancel_conversion(self):
        """변환 중단"""
        self.converter.stop_conversion()
        self.progress_var.set("변환이 중단되었습니다.")
        self.convert_button.config(state='normal')
        self.cancel_button.config(state='disabled')
