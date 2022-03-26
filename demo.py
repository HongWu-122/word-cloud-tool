import wordcloud
import jieba
import imageio
# import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
import os
from tkinter.filedialog import *
import webbrowser

num = 1
txt = 'demo.txt'
jpg = 'demo.jpg'
ttf = 'STLITI.TTF'

# 点击“选择文件夹”按钮调用该功能
def select_files(pathin):
    path = askdirectory(title='选择文件夹')
    pathin.set(path.strip()) # strip() 用于移除字符串头尾指定的字符（默认为空格或者换行符）或字符序列，只能是移除字符串开头和结尾部分

# 点击“选择文件”按钮调用该功能
def select_file(pathin):
    path = askopenfilename(title='选择文件')
    pathin.set(path.strip()) # strip() 用于移除字符串头尾指定的字符（默认为空格或者换行符）或字符序列，只能是移除字符串开头和结尾部分

def find():  # 查找
    global text,window
    t = Toplevel()
    t.title('查找')
    # 设置窗口大小
    t.geometry('260x60+200+250')
    t.transient(window)
    Label(t, text='查找:').grid(row=0, column=0, sticky='e')
    v = StringVar()
    e = Entry(t, width=20, textvariable=v)
    e.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    e.focus_set()
    c = IntVar()
    Checkbutton(t, text='不区分大小写', variable=c).grid(row=1, column=1, sticky='e')
    Button(t, text='查找所有', command=lambda: search(e.get(), c.get(), text, t, e)).grid(row=0, column=2,sticky='e' + 'w', padx=2,pady=2)
    def close_search():
        text.tag_remove('match', '1.0', END)
        t.destroy()
    t.protocol('WM_DELETE_WINDOW', close_search)

def search(needle, cssnstv, text, t, e):  # 搜索
    text.tag_remove('match', '1.0', END)
    count = 0
    if needle:
        pos = '1.0'
        while True:
            pos = text.search(needle, pos, nocase=cssnstv, stopindex=END)
            if not pos: break
            lastpos = pos + str(len(needle))
            text.tag_add('match', pos, lastpos)
            count += 1
            pos = lastpos
        text.tag_config('match', foreground='red', background='yellow')
        e.focus_set()
        t.title(str(count) + '个被匹配')

def analysis(txt,jpg):
    try:
        global text
        # 设置文本框初始内容
        text.config(state=NORMAL)  # 开启可写入模式
        text.delete(0.0, END)
        text.insert('insert', "{1:{0}<8}{2:{0}^8} \n".format(chr(12288), '提取词语', '词频次数'))
        t=open(txt,"r",encoding='utf-8').read()
        words=jieba.lcut(t)
        counts={}
        for word in words:
            if len(word)==1:
                continue
            else:
                counts[word]=counts.get(word,0)+1
        items=list(counts.items())
        items.sort(key=lambda x:x[1],reverse=True)
        # text.config(state=NORMAL)  # 开启可写入模式
        try:
            for i in range(20853):
                word,count=items[i]
                # print("{0:<10} {1:>10}".format(word,count))
                content = "{1:{0}<8}{2:{0}^8} \n".format(chr(12288),word,count)
                # print(content)
                # 设置文本框内容
                text.insert('insert', content)
                text.update()  # 插入后及时的更新
                # text.see(END)  # 使得聊天记录text默认显示底端
            text.config(state=DISABLED)  # 关闭可写入模式 # 不能编辑
        except:
            text.config(state=DISABLED)  # 关闭可写入模式 # 不能编辑
    except Exception as error:
        messagebox.showinfo("报错提示","错误是{}，也许是文件被移动或不存在或文件名字不一致".format(error))

def picture(win_cloud,txt,jpg,ttf):
    global num
    try:
        messagebox.showinfo('小提示', '正在分析文本并生成词云图，稍等一小会')
        # try:
        f = open(txt, "r", encoding="utf-8")
        img = imageio.imread(jpg)
        r = f.read()
        f.close()
        ls = jieba.lcut(r)
        r = ' '.join(ls)
        try:
            w = wordcloud.WordCloud(width=400, height=200, background_color="white", font_path=ttf,mask=img)
        except:
            messagebox.showinfo('小提示', '没有找到.ttf字体文件，默认')
            w = wordcloud.WordCloud(width=400, height=200, background_color="white",mask=img)

        # m默认像素宽400 高200 背景颜色黑
        '''#font_path指的是字体文件路径，
           #因为wordcloud自带的字体不支持中文所以我们要指定一个字体文件，
           #否者输出的图片全是框框'''
        # background_color 默认是黑色　我设置成白色
        # max_words最大显示的词数
        # mask 背景图片
        # max_font_size　最大字体字号
        w.generate(r)
        # path = os.getcwd()
        # path = os.path.split(jpg)[0] + '/词云图{}.jpg'.format(num)
        path = '词云图{}.jpg'.format(num)
        num += 1
        w.to_file(path)
        messagebox.showinfo('小提示', '词云图生成成功，位置在{}'.format(path))

        analysis(txt, jpg)
        os.system("start " + path)

        win_cloud.mainloop()
    except Exception as error:
        messagebox.showinfo("报错提示","错误是{}，也许是文件被移动或不存在或文件名字不一致".format(error))

def author():
    if messagebox.askokcancel('小提示', '作者：小鸿武\n时间：2022年3月26日\n版本：V1.0'
                                     '\n点击‘确定’跳转到项目开源地址：https://github.com/HongWu-122/word-cloud-tool'):
        url = 'https://github.com/HongWu-122/word-cloud-tool'
        webbrowser.open(url=url, new=0)

def error_information():
    messagebox.showinfo('教程指导','1.生成图片”生非所样“：建议换图片试试，图片背景挖空/纯白底，背景和图案颜色色彩差别大一点为佳；\n'
                               '2.“.ttf”后缀的文件是必要的生成字体文件，可以更换其他字体文件，但不能缺少\n'
                               '3.生成词云图片为软件运行文件夹路径下，文件名字为“词云图+已生成数量编号”\n'
                               '4.一般报错都是文件路径出了问题，文件名错误/文件不存在/对应文件类型不正确/\n'
                               '5.文件类型：数据文件用记事本“.txt“后缀的；背景图片用“.jpg”或“.png”的图片文件类型；'
                               '字体文件是“.ttf”后缀的文件；其他字体请百度搜索具体内容\n'
                               '')

def word_cloud(txt,jpg,ttf):
    global text,window
    try:
        window = Tk()
        window.geometry("465x500+700+60")
        # 禁止窗口的拉伸
        # window.resizable(0, 0)
        # 窗口的标题
        window.title("词频分析V1.0   By HONGWU")
        # messagebox.showinfo('小提示', '这是一个自动生成词云图和词云分析的程序 By HONGWU')

        frame = Frame(window, height=160, width=450, bd=1, bg='Pink')  # , bg='gray97'
        frame.place(x=0,y=0)

        label1 = Label(frame, text="txt：", bg='Pink')
        label1.place(x=10, y=10)
        label2 = Label(frame, text="jpg/png：", bg='Pink')
        label2.place(x=5, y=40)
        label1 = Label(frame, text="ttf：", bg='Pink')
        label1.place(x=10, y=70)
        # 输入框
        pathin1 = StringVar()  # 定义变量
        entry1 = Entry(frame, textvariable=pathin1)  # 输入框
        entry1.place(x=60, y=10, width=280)
        pathin1.set(txt)
        pathin2 = StringVar()  # 定义变量
        entry2 = Entry(frame, textvariable=pathin2)  # 输入框
        entry2.place(x=60, y=40, width=280)
        pathin2.set(jpg)
        pathin3 = StringVar()  # 定义变量
        entry3 = Entry(frame, textvariable=pathin3)  # 输入框
        entry3.place(x=60, y=70, width=280)
        pathin3.set(ttf)

        button1 = Button(frame, text='选择数据文本', command=lambda: select_file(pathin1), bg='LightGreen')
        button1.place(x=355, y=7)
        button2 = Button(frame, text='选择背景图片', command=lambda: select_file(pathin2), bg='SkyBlue')
        button2.place(x=355, y=37)
        button3 = Button(frame, text='选择字体文件', command=lambda: select_file(pathin3), bg='lavender')
        button3.place(x=355, y=67)
        button3 = Button(frame, text='点击生成词云图', command=lambda:picture(window,pathin1.get(),pathin2.get(),pathin3.get()), bg='wheat')
        button3.place(x=240, y=97,height=40,width=200)

        frame2 = Frame(window, height=360, width=450, bd=1, bg='Pink')  # , bg='gray30'
        frame2.place(x=0,y=140)

        # 创建滚动条
        scroll = Scrollbar(window)
        # 创建文本框
        text = Text(frame2, font=('微软雅黑', '12'))
        text.place(x=3,y=0, width=440, height=300)
        # 设置文本框初始内容
        text.insert('insert', "{1:{0}<8}{2:{0}^8} \n".format(chr(12288), '提取词语', '词频次数'))
        text.update()  # 插入后及时的更新
        text.config(state=DISABLED) # 不能编辑

        x = 20
        button4 = Button(frame2, text='点击词频数分析',font=('微软雅黑',10), command=lambda : analysis(pathin1.get(), pathin2.get()), bg='wheat')
        button4.place(x=x,y=315)
        button5 = Button(frame2, text='定位查找关键词', font=('微软雅黑', 10), command=find, bg='wheat')
        button5.place(x=x+120, y=315)
        button6 = Button(frame2, text='教程指导', font=('微软雅黑', 10), command=error_information, bg='wheat')
        button6.place(x=x+250, y=315)
        button6 = Button(frame2, text='版本信息', font=('微软雅黑', 10), command=author, bg='wheat')
        button6.place(x=x+340, y=315)

        # Checkbutton(t, text='不区分大小写', variable=c).grid(row=1, column=1, sticky='e')
        # 将滚动条和文本框分别填充
        scroll.pack(side=RIGHT, fill=Y)# side指定Scrollbar为居右；fill指定填充满整个剩余区域 # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
        # text.pack(expand=YES,side=LEFT,fill=X) # 将文本框填充进窗口的左侧 # expand=YES 支持扩张yes   fill=BOTH 填充XY
        # 将滚动条与文本框互相关联
        scroll.config(command=text.yview)# 指定Scrollbar的command的回调函数是Listbar的yview # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
        text.config(yscrollcommand=scroll.set, state=DISABLED) # 将滚动条关联到文本框 # 设置text禁止用户对其显示的内容编辑 state=DISABLED

        window.mainloop()

    except Exception as error:
        messagebox.showinfo("报错提示","错误是{}，也许是文件被移动或不存在或文件名字不一致".format(error))


if __name__ == '__main__':
    word_cloud(txt,jpg,ttf)

"""
WordCloud参数讲解：
            font_path表示用到字体的路径
            width和height表示画布的宽和高
            prefer_horizontal可以调整词云中字体水平和垂直的多少
            mask即掩膜，产生词云背景的区域
            scale:计算和绘图之间的缩放
            min_font_size设置最小的字体大小
            max_words设置字体的多少
            stopwords设置禁用词
            background_color设置词云的背景颜色
            max_font_size设置字体的最大尺寸
            mode设置字体的颜色 但设置为RGBA时背景透明
            relative_scaling设置有关字体大小的相对字频率的重要性
            regexp设置正则表达式
            collocations 是否包含两个词的搭配


常见参数保存
background_color	示例：background_color=‘white’，说明：指定背景色,可以使用16进制颜色
width	示例：width=600	说明：指定图像长度 ，图像长度默认400 单位像素
height	示例：height=400	说明：指定图像高度图像高度 默认200
margin	示例：margin=20	说明：词与词之间的边距 默认2
scale	示例：scale=0.5	说明：缩放比例 对图像整体进行缩放 默认为1
prefer_horizontal	示例：prefer_horizontal=0.9	说明：词在水平方向上出现的频率,默认为0.9
min_font_size	示例：min_font_size=10说明：	最小字体 默认为4
max_font_size	示例：max_font_size=20	说明：最大字体 默认为200
font_step	示例：font_step=2	说明：字体步幅 控制在给定text遍历单词的步幅 默认为1 一般不用修改 对于较大text 增大font_step会加快读取速度 但会牺牲部分准确性
stopwords	stopwords=set(‘dog’)	设置要过滤的词 以字符串或者集合作为接收参数 如不设置将使用默认的 停动词词库 这个试过了，没成功
mode	示例：mode='RGB’说明：	设置显色模式 默认RGB 如果为RGBA且background_color不为空时，背景为透明
relative_scaling	示例：relative_scaling=1	说明：词频与字体大小关联性 默认为5 值越小 变化越明显
color_func	示例：color_func=None	说明：生成新颜色的函数 如果为空 则使用 self.color_func
regexp	示例：regexp=None	说明：默认单词是以空格分割,如果设置这个参数 将根据指定函数来分割
width	示例：regexp=None	说明：默认400 单位像素
collocations	示例：collocations=False	说明：是否包含两个词的搭配 默认为True
colormap	示例：colormap=None	说明：给所有单词随机分配颜色 指定color_func则忽略
random_state	示例：random_state=1	说明：为每个单词返回一个PIL颜色
font_path	示例：font_path=‘PangMenZhengDaoBiaoTiTi-1.ttf’	说明：指定字体
mask	示例：mask=mask_pic	说明：指定背景图,会将单词填充在背景图像素非白色(#FFFFFF RGB(255,255,255))的地方
"""
