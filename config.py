# -*- coding: utf-8 -*-
"""설정 및 상수 정의"""

# 지원하는 이미지 형식
SUPPORTED_FORMATS = {
    'PNG': '*.png',
    'JPEG': '*.jpg;*.jpeg',
    'BMP': '*.bmp',
    'GIF': '*.gif',
    'TIFF': '*.tiff;*.tif',
    'WEBP': '*.webp',
    'ICO': '*.ico'
}

# ICO 크기 옵션 (가장 높은 화질인 256px만 유지)
ICO_SIZES = [256]

# 기본 설정
DEFAULT_SETTINGS = {
    'auto_crop': True,
    'crop_threshold': 15,
    'icon_scale': 90,
    'allow_upscale': True,
    'resample_method': 'LANCZOS',
    'background_mode': 'transparent',
    'selected_sizes': [256] # 기본 선택 크기를 256px로 변경
}

# 리샘플링 방법 설명
RESAMPLE_DESCRIPTIONS = {
    "LANCZOS": "LANCZOS: 최고 화질, 가장 선명 (권장)",
    "BICUBIC": "BICUBIC: 고화질, 부드러운 결과",
    "BILINEAR": "BILINEAR: 빠른 처리, 기본 화질"
}