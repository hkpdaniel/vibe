import tkinter as tk
from tkinter import messagebox
import re
import winsound

# 1. 메인 윈도우 설정 (GUI)
root = tk.Tk()
root.title("IT26Vibe Unit-Switcher")
root.geometry("350x200")
root.attributes("-topmost", True)  # 항상 다른 창 위에 표시

# 2. 변환 데이터 설정 (기계공학용)
CONVERSION_FACTORS = {
    'psi': ('Pa', 6894.76),
    'lb': ('kg', 0.453592),
    'inch': ('mm', 25.4),
    'kgf': ('N', 9.80665)
}

last_clipboard = ""

# 화면 표시용 텍스트
label = tk.Label(root, text="🚀 단위 변환기 작동 중", font=("Arial", 14, "bold"), pady=20)
label.pack()
info = tk.Label(root, text="psi, lb, inch 등을 복사해 보세요!", fg="gray")
info.pack()

def check_clipboard():
    global last_clipboard
    try:
        # 클립보드 내용 읽기 (tkinter 기본 기능 사용)
        current_text = root.clipboard_get().strip().lower()
        
        # 새로운 내용이 복사되었을 때만 실행
        if current_text != last_clipboard:
            # 정규표현식으로 숫자와 단위 추출 (예: 100psi, 50 lb)
            match = re.match(r"([0-9.]+)\s*([a-zA-Z]+)", current_text)
            
            if match:
                value = float(match.group(1))
                unit = match.group(2)
                
                if unit in CONVERSION_FACTORS:
                    target_unit, factor = CONVERSION_FACTORS[unit]
                    result_val = round(value * factor, 2)
                    result_text = f"{result_val} {target_unit}"
                    
                    # 클립보드 다시 쓰기
                    root.clipboard_clear()
                    root.clipboard_append(result_text)
                    last_clipboard = result_text # 무한 루프 방지
                    
                    # 알림음 및 메시지 박스 (GUI)
                    winsound.Beep(1000, 200)
                    messagebox.showinfo("변환 완료", f"원래 값: {current_text}\n변환 값: {result_text}")
                else:
                    last_clipboard = current_text
            else:
                last_clipboard = current_text
    except:
        # 클립보드가 비어있거나 텍스트가 아닐 경우 예외 처리
        pass
    
    # 0.5초마다 클립보드 체크 (이벤트 루프)
    root.after(500, check_clipboard)

# 3. 실행
print("Unit-Switcher가 시작되었습니다. 창을 끄지 마세요.")
check_clipboard()
root.mainloop()