from screeninfo import get_monitors 

def get_current_monitor(window): # Returns the current screen info Monitor object the window is on 
    window.update_idletasks()
    x, y = window.winfo_x(), window.winfo_y()
    for m in get_monitors():
        if m.x <= x < m.x + m.width and m.y <= y < m.y + m.height:
            return m 
    return get_monitors()[0]

def fit_current_screen(window):
    m = get_current_monitor(window)
    window.geometry(f"{m.width}x{m.height}+{m.x}+{m.y}")
