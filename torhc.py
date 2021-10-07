verbose_decode=0
indent = '    '
def get(n):
    return n.read(1).decode('ascii')
def peek(n):
    import os
    ch = get(n)
    n.seek(-1,os.SEEK_CUR)
    return ch
def decode_string(n,depth):
    str_size=''
    ch = get(n)
    assert ch.isdigit()
    while ch.isdigit():
        str_size+=ch
        ch = get(n)
    assert ch==":"
    size=int(str_size)
    r=n.read(size)
    try:
        r=r.decode('utf-8')
    except:
        pass
        #r='bytestring'
    if (verbose_decode):
        print(indent*depth+r)
    #sl.append(r)
    return (r)

def decode_integer(n,depth):
    ch = get(n)
    assert ch=='i'
    ch = get(n)
    str=''
    while ch.isdigit():#What about neg numbers?
        str+=ch
        ch = get(n)
    assert ch=='e'
    i = int(str)
    if verbose_decode: print(indent*depth+str)
    return i

def decode_list(n,depth):
    if verbose_decode: print(indent*depth+"list{")
    ch = get(n)
    assert ch=='l'
    l=[]
    while peek(n)!='e':
        temp = decode_item(n,depth+1)
        assert temp!=None
        l.append(temp)
    ch = get(n)
    assert ch=='e'
    if verbose_decode:    print(indent*depth+"}")
    return l
def decode_dictionary(n,depth):
    m={}
    if verbose_decode:    print(indent*depth+"map{")
    ch = get(n)
    assert ch=='d'
    while peek(n).isdigit():
        s=decode_string(n,depth+1)
        assert s!=None
        temp = decode_item(n,depth+1)
        assert temp!=None
        m[s]=temp
        if verbose_decode: print()
    ch=get(n)
    assert ch=='e'
    if verbose_decode: print(indent*depth+"}")
    return m
def decode_item(n,depth):
    switch_map={
    'd':decode_dictionary,
    'i':decode_integer,
    'l':decode_list,
    '0':decode_string,
    '1':decode_string,
    '2':decode_string,
    '3':decode_string,
    '4':decode_string,
    '5':decode_string,
    '6':decode_string,
    '7':decode_string,
    '8':decode_string,
    '9':decode_string,
    }
    ch=peek(n)
    func=switch_map[ch]
    return func(n,depth)
def decode_item_from_file(fn):
    handle=open(fn,'rb')
    r=decode_item(handle,0)
    handle.close()
    return r
def textdump_bt_item(n,depth=0):
    from datetime import datetime
    if type(n)==int:
        return indent*depth+str(n)+'\n'
    if type(n)==str:
        return indent*depth+n+'\n'
    rv=''
    if type(n)==dict:
        rv+=indent*depth+'map{\n'
        for key,value in n.items():
            if key=='creation date':
                rv+=indent*(depth+1)+key+'\n'
                rv+=indent*(depth+1)+str(datetime.fromtimestamp(value))+'\n\n'
            elif key=='pieces':
                rv+=indent*(depth+1)+key+'\n'
                pieces=binascii.hexlify(value).decode('utf-8')
                v=[pieces[i:i+40] for i in range(0,40,40)]
                for e in v:
                    rv+=indent*(depth+1)+e+'\n'
            else:
                rv+=indent*(depth+1)+key+'\n'
                rv+=textdump_bt_item(value,depth+1)+'\n'
        rv+=indent*depth+'}\n'
        return rv
    if type(n)==list:
        rv+=indent*depth+'list{\n'
        for each in n:
            rv+=textdump_bt_item(each,depth+1)
        rv+=indent*depth+'}\n'
        return rv

def multi_join(v):
    import os
    r=v[0]
    for i in range(1,len(v)):
        r+=os.path.join(r,v[i])
    return r
def get_file_list(bt):
    if 'files' in bt['info']:
        #fl=[]
        #for each in bt['info']['files']:
        #    fl.append(multi_join(each['path']))
        #return fl
        return [multi_join(each['path']) for each in bt['info']['files']]
    else:
        return [bt['info']['name']]
def get_name(fn):
    try:
        bt=decode_item_from_file(fn)
        return bt['info']['name']
    except:
        pass

import sys
import binascii
def main():

    try:
         fn=sys.argv[1]
    except:
         return
    try:
        btitem=decode_item_from_file(fn)
        text=textdump_bt_item(btitem)
        #print('textdump=\n'+text)
    except:
        pass
    print('04 get func.py')

    input()
def tkinter_print():
    global btitem
    global text
    global sl
    try:
        fn=sys.argv[1]
    except:
        return
    btitem=decode_item_from_file(fn)
    text=textdump_bt_item(btitem)
    flv=get_file_list(btitem)
    text+=('\n').join(flv)

    import tkinter as tk
    import tkinter.scrolledtext as scrolledtext
    root=tk.Tk()
    root.geometry("1500x900+0+0")
    T=scrolledtext.ScrolledText(root)
    T['font'] = ('consolas', '12')
    T.pack(expand=True,fill="both")
    #S.pack(side=tk.RIGHT,fill=tk.Y)
    #S.config(command=T.yview)
    #T.config(yscrollcommand=S.set)
    T.insert(tk.END,text)
    root.mainloop()
def search(n):
    sdir=r'C:\Users\X\AppData\Local\qBittorrent\BT_backup'
    import os
    import shutil
    global v
    v=os.listdir(sdir)
    global w
    w=[fn for fn in v if os.path.splitext(fn)[1]=='.torrent']
    for fn in w:
        src=os.path.join(sdir,fn)
        if get_name(src)==n:
            shutil.copy(src,
                        os.path.join(input("copy dest?: "),
                                     n+'.torrent')
                        )
            print('copied')
def rename_torrents_in_dir():
    try:
        dir=sys.argv[1]
    except:
        return
    import os
    for fn in os.listdir(dir):
        if os.path.splitext(fn)[1]!='.torrent': continue
        newfn = get_name(os.path.join(dir,fn))+".torrent"
        print(fn,newfn)
        if newfn:
            os.rename(os.path.join(dir,fn),os.path.join(dir,newfn))
if __name__ == '__main__':
    tkinter_print()
