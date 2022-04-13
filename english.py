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

# s_origin = """
# Even though Alexander was talking about patterns in buildings and towns, 
# what he says is true about object-oriented design patterns. 
# Our solutions are expressed in terms of objects and interfaces instead of walls and doors, 
# but at the core of both kinds of patterns is a solution to a problem in a context.
# """

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
        for s in lst:
            s = re.sub('-', '- ', s)
            s = s.strip()
            if s:
                result += fun(s, *args, **kwargs)
        txt2.delete("0.1",tk.END)
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

root = tk.Tk()
root.title("IPA reading of English text")
root.geometry("+5+5")
txt1 = tk.Text(root, height=8, wrap='word', font=('Times', 16))
txt2 = tk.Text(root, wrap='word',font=('Times', 16))
btnExit = tk.Button(root,text="Exit", command=sys.exit)
frame = tk.Frame(root)
btn1 = tk.Button(frame,text="Transform simple", command=transform_simple)
btn2 = tk.Button(frame,text="Transform normal", command=transform_normal)
btn3 = tk.Button(frame,text="Transform list", command=transform_list)
txt1.grid(row=0,column=0)
txt2.grid(row=1,column=0, sticky='we')
btnExit.grid(row=0,column=1, sticky='nwe')
frame.grid(row=1,column=1, sticky='n')
btn1.pack(fill=tk.X)
btn2.pack(fill=tk.X)
btn3.pack(fill=tk.X)
txt1.insert(tk.END,s_origin)

tk.mainloop()