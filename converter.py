# -*- coding: utf-8 -*-
"""이미지 변환 로직"""

import os
import numpy as np
from PIL import Image
import traceback

class ImageConverter:
    def __init__(self):
        self.is_converting = False
    
    def stop_conversion(self):
        """변환 중단"""
        self.is_converting = False
    
    def smart_crop(self, img, threshold=15):
        """스마트 여백 제거"""
        try:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            img_array = np.array(img)
            
            if img_array.shape[2] == 4:  # RGBA
                alpha = img_array[:, :, 3]
                non_transparent = alpha > threshold
                
                rgb = img_array[:, :, :3]
                not_white = np.any(rgb < (255 - threshold), axis=2)
                
                content_mask = non_transparent & not_white
            else:  # RGB
                rgb = img_array[:, :, :3]
                not_white = np.any(rgb < (255 - threshold), axis=2)
                content_mask = not_white
            
            if np.any(content_mask):
                rows = np.any(content_mask, axis=1)
                cols = np.any(content_mask, axis=0)
                
                if np.any(rows) and np.any(cols):
                    top = np.argmax(rows)
                    bottom = len(rows) - np.argmax(rows[::-1]) - 1
                    left = np.argmax(cols)
                    right = len(cols) - np.argmax(cols[::-1]) - 1
                    
                    if top <= bottom and left <= right:
                        return img.crop((left, top, right + 1, bottom + 1))
            
            return img
            
        except Exception as e:
            print(f"스마트 크롭 오류: {e}")
            return img
    
    def resize_for_icon(self, img, target_size, resample_method, scale_percent=90, allow_upscale=True):
        """아이콘 크기로 리사이즈"""
        try:
            # 리샘플링 방법 설정
            try:
                resample_map = {
                    'LANCZOS': Image.Resampling.LANCZOS,
                    'BICUBIC': Image.Resampling.BICUBIC,
                    'BILINEAR': Image.Resampling.BILINEAR,
                }
            except AttributeError:
                resample_map = {
                    'LANCZOS': Image.LANCZOS,
                    'BICUBIC': Image.BICUBIC,
                    'BILINEAR': Image.BILINEAR,
                }
            
            resample = resample_map.get(resample_method, resample_map['LANCZOS'])
            
            icon_size = int(target_size * scale_percent / 100)
            padding = (target_size - icon_size) // 2
            
            # 업스케일링 제한 확인
            if not allow_upscale and icon_size > max(img.size):
                scale_factor = max(img.size) / icon_size
                icon_size = int(icon_size * scale_factor)
                padding = (target_size - icon_size) // 2
            
            # 이미지 리사이즈
            img_resized = img.resize((icon_size, icon_size), resample)
            
            # 투명 배경으로 결과 이미지 생성
            result = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
            
            # 이미지 붙이기
            if img_resized.mode == 'RGBA':
                result.paste(img_resized, (padding, padding), img_resized)
            else:
                result.paste(img_resized, (padding, padding))
            
            return result
            
        except Exception as e:
            print(f"리사이즈 오류: {e}")
            return img.resize((target_size, target_size))
    
    def convert_to_ico(self, input_path, output_path, settings):
        """이미지를 ICO로 변환"""
        try:
            print(f"변환 시작: {os.path.basename(input_path)}")
            
            with Image.open(input_path) as img:
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # 스마트 크롭
                if settings.get('auto_crop', True):
                    img = self.smart_crop(img, settings.get('crop_threshold', 15))
                
                images = []
                sizes = settings.get('selected_sizes', [256])
                
                # 각 크기별 아이콘 생성
                for size in sizes:
                    if not self.is_converting:
                        return False
                    
                    try:
                        icon_img = self.resize_for_icon(
                            img, size, 
                            settings.get('resample_method', 'LANCZOS'),
                            settings.get('icon_scale', 90),
                            settings.get('allow_upscale', True)
                        )
                        images.append(icon_img)
                        print(f"✅ {size}px 생성 완료")
                    except Exception as e:
                        print(f"❌ {size}px 생성 실패: {e}")
                
                # ICO 파일 저장
                if images:
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    
                    images[0].save(
                        output_path,
                        format='ICO',
                        sizes=[(img.size[0], img.size[1]) for img in images]
                    )
                    
                    print(f"✅ 저장 완료: {output_path}")
                    return True
                
                return False
                
        except Exception as e:
            print(f"❌ 변환 실패: {e}")
            traceback.print_exc()
            return False
    
    def convert_multiple(self, file_list, output_dir, settings, progress_callback=None):
        """여러 파일 일괄 변환"""
        self.is_converting = True
        success_count = 0
        total_files = len(file_list)
        
        try:
            for i, input_path in enumerate(file_list):
                if not self.is_converting:
                    break
                
                # 진행률 콜백
                if progress_callback:
                    progress_callback(i, total_files, os.path.basename(input_path))
                
                # 출력 파일명 생성
                filename = os.path.splitext(os.path.basename(input_path))[0]
                if output_dir == "원본 파일과 같은 폴더":
                    output_path = os.path.join(os.path.dirname(input_path), f"{filename}.ico")
                else:
                    output_path = os.path.join(output_dir, f"{filename}.ico")
                
                # 변환 실행
                if self.convert_to_ico(input_path, output_path, settings):
                    success_count += 1
            
            return success_count, total_files
            
        except Exception as e:
            print(f"일괄 변환 오류: {e}")
            return success_count, total_files
        
        finally:
            self.is_converting = False
