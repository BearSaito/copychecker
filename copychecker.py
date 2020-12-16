import sys
import os
import glob
from difflib import Differ, SequenceMatcher # 類似度算出
import argparse  # オプション

debug = False

'''ファイルのpathを取得'''
def getfilename(path):
    filename = sorted([f for f in glob.glob(f"{path}")], key=str.lower)
    return filename

'''ファイル読み込み'''
def readfile(path, fill, sortbool):
    line = []
    error = 0
    for enc in ['shift_jis', 'utf_8', 'utf_8_sig']: # encode
        try:
            with open(path, 'r', encoding = enc) as fileobj:
                line = fileobj.readlines() #全文読み込み
                if(fill == True):line = [mono.replace("\t", "").replace(" ", "") for mono in line] # タブ，スペース除去
                if(sortbool == True):line.sort() # 文字ソート
        except UnicodeDecodeError: # encodeが違う場合，Errorを無視
            error += 1
    if (debug == True):print(f"error:{error}, path:{path}")
    return line

'''差分を表示'''
def showdiff(text1_lines, text2_lines):
    print(f"\ndiff:\n")
    d = Differ()
    diff = d.compare(text1_lines, text2_lines)
    print('\n'.join(diff))

'''類似度を算出'''
def showratio(text1_lines,text2_lines):
    ratio = SequenceMatcher(lambda x: x == " ", text1_lines, text2_lines).ratio()
    print(f"\nRatio：\n小数第5位：{round(ratio,5)}\n全て 　　：{ratio}")  # 結果の表示用
    return ratio

'''結果出力'''
def writefile(result,path):
    with open(path, 'w', encoding='utf_8') as fileobj:
        fileobj.writelines(result)

'''main'''
def main(args):
    lebel = ''.join(["/*" for i in range(args.lebel)])
    print(lebel)
    filenamelist = getfilename(f"{args.path.rstrip('/')}{lebel}.{args.ext}")
    print(filenamelist)
    result = [f'{"-"*100}\n']
    for num,text1 in enumerate(filenamelist):
        print("★"*100)
        text1_lines = readfile(text1, args.fill, args.sort)
        for i in range(num, len(filenamelist)):
            text2 = filenamelist[i]
            if (text1 != text2):
                text2_lines = readfile(text2, args.fill, args.sort)
                print(f"text1：{text1}：text2：{text2}") # 類似度を算出するファイル # debug
                ratio = showratio(text1_lines, text2_lines)
                if(ratio >= args.border):
                    if(args.diff == True):showdiff(text1_lines, text2_lines) # 差分を表示
                    result.append(f"ratio：{ratio}\n{text1}\n{text2}\n\n")
            print(f'{"-"*100}') # 表示用
        if(f'{"-"*100}\n' not in result[-1]):result.append(f'{"-"*100}\n')
    if (args.rank == True): result.sort(reverse=True)  # ratioが降順にソート
    [print(mono, end="") for mono in result]  # border以上のratioの結果を表示s
    if(args.out == ''):
        args.out = f"{os.path.split(args.path.rstrip('/')+'/')[0]}/result_similar.txt"
    writefile(result, args.out)  # resultのリストのみをファイルに書き出す

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='copychecker')
    parser.add_argument('-p', '--path', default='./programs/',
                        help='ディレクトリ名')
    parser.add_argument('-l', '--lebel', type=int, default=1,
                        help='ディレクトリの階層')
    parser.add_argument('-e', '--ext', default='c',
                        help='拡張子')
    parser.add_argument('-o', '--out', default='',
                        help='結果を出力するファイル名')
    parser.add_argument('-b', '--border', type=float, default=0.5,
                        help='類似度の境界線（初期値：0.5）')
    parser.add_argument('-s', '--sort', action='store_true',
                        help='プログラムの行をソートして比較')
    parser.add_argument('-d', '--diff', action='store_true',
                        help='差分を表示')
    parser.add_argument('-r', '--rank', action='store_true',
                        help='類似度を降順で表示')
    parser.add_argument('-f', '--fill', action='store_true',
                        help='タブと空白を除去')

    args = parser.parse_args()
    main(args)