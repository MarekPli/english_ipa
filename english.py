from tkinter.font import ITALIC
import eng_to_ipa
import tkinter as tk
import re
import sys
s_origin = """
Once upon a midnight dreary, while I pondered, weak and weary,
Over many a quaint and curious volume of forgotten lore-
While I nodded, nearly napping, suddenly there came a tapping,
As of some one gently rapping, rapping at my chamber door.
"'Tis some visitor," I muttered, "tapping at my chamber door-
Only this and nothing more."
"""
def comma_use(lst):
    if lst[0][-1] not in ",.-;": # not only alpha, because IPA is not only alpha
        return f"[{', '.join(lst)}]"
    lst2 = [x[:-1] for x in lst]
    return f"[{', '.join(lst2)}]{lst[0][-1]}"

def transforming(fun, *args, **kwargs):
    def inner(*args, **kwargs):
        txt = txt1.get("0.1", tk.END)
        result = ''
        lst = txt.split('\n')
        txt2.delete("0.1",tk.END)
        for s in lst:
            s = re.sub('-', '- ', s)
            s = s.strip()
            if s:
                result += fun(s, *args, **kwargs)
        
        lsts = result.split('\n\n')
        if len(lsts) > 1:
            for lst in lsts:
                s = lst.split('\n')
                if len(s) > 1:
                    txt2.insert(tk.END,s[0] + '\n', 'bold')
                    txt2.insert(tk.END,s[1] + '\n\n')
                else: 
                    txt2.insert(tk.END,lst + '\n')
        else:
            txt2.insert(tk.END,result)
    return inner

@transforming
def transform_simple(txt):
    return f"{eng_to_ipa.convert(txt)}\n"

@transforming
def transform_normal(txt):
    return f"{txt}\n{eng_to_ipa.convert(txt)}\n\n"

@transforming
def transform_list(txt):
    res_l = eng_to_ipa.ipa_list(txt)  
    m = []
    for r in res_l:
        if len(r) > 1:
            # m.append(str(r))
            m.append(comma_use(r))
        else: m.append(r[0])

    res = ' '.join(m)
    return f"{txt}\n{res}\n\n"


def alarmed():
    if not txt1.tag_ranges('sel'):
        return
    if tk.SEL_FIRST and tk.SEL_LAST:
        s = txt1.get(tk.SEL_FIRST, tk.SEL_LAST)
        print(s)
    
def search_word():
    x = txt1.tag_ranges('sel')
    if x:
        s=txt1.get(x[0], x[1])
        labelIPA['text'] = f"{eng_to_ipa.convert(s)}"

    # print("selected")
        # alarmed()
    # root.after(1000, alarmed)
    # return 'break'
    # print(txt1.get(*ranges))

root = tk.Tk()
root.title("IPA reading of English text")
root.geometry("+5+5")
txt1 = tk.Text(root, height=8, wrap='word', font=('Times', 16), padx=10, pady=10)
txt2 = tk.Text(root, wrap='word',font=('Times', 16), padx=10, pady=15)
txt2.tag_configure('bold', font=('Times', 16, 'bold'))

# txt2.bind('<Double-Button-1>', lambda: print('jajko'))
# txt1.bind('<Button-1>', lambda ev: search_word())
# txt1.bind('<Double-Button-1>', lambda ev: search_word())
txt1.bind('<<Selection>>', lambda ev: search_word())
# txt1.bind('<KeyPress>', lambda ev: search_word())
    
frame = tk.Frame(root)
btnExit = tk.Button(frame,text="Exit", command=sys.exit)
frame.grid(row=0,column=1, sticky='nwe')
btnExit.pack(fill=tk.X)
frame = tk.Frame(root)
btn1 = tk.Button(frame,text="Transform simple", command=transform_simple)
btn2 = tk.Button(frame,text="Transform normal", command=transform_normal)
btn3 = tk.Button(frame,text="Transform list", command=transform_list)
txt1.grid(row=0,column=0)
txt2.grid(row=2,column=0, sticky='we')
frame.grid(row=2,column=1, sticky='n')
btn1.pack(fill=tk.X)
btn2.pack(fill=tk.X)
btn3.pack(fill=tk.X)
labelIPA = tk.Label(root, font=('Arial', 16))
labelIPA.grid(row=1,column=0)
txt1.insert(tk.END,s_origin)

tk.mainloop()