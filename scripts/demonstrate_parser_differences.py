"""異なるパーサが同じマークアップをどのように解析するかをデモンストレーションします。

Beautiful Soupは、異なるパーサーのいずれかを使用することができます。すべての
パーサは、有効なマークアップに対しては多かれ少なかれ同じ振る舞いをしなければなりません。
Beautiful Soupのユニットテストは、これを確認しています。しかし、すべての
パーサは無効なマークアップを異なる方法で処理します。異なるバージョンの
同じパーサーでも、無効なマークアップの扱いが異なります。そのため、ユニット
テストがあるにもかかわらず、私はこの教育用デモスクリプトを作成しました。

demonstration_markup.txtファイルには何行ものHTMLが含まれています。この
スクリプトは、マークアップの各行をあなたがインストールしたすべてのパーサに対してテストします。
各パーサがそのマークアップをどのように見ているかを表示します。これは
パーサーを選択、
もしくは、Beautiful Soupの動作の理解に役立ちます。

"""

import os
import sys
from bs4 import BeautifulSoup
parsers = ['html.parser']

try:
    from bs4.builder import _lxml
    parsers.append('lxml')
except ImportError, e:
    pass

try:
    from bs4.builder import _html5lib
    parsers.append('html5lib')
except ImportError, e:
    pass

class Demonstration(object):
    def __init__(self, markup):
        self.results = {}
        self.markup = markup

    def run_against(self, *parser_names):
        uniform_results = True
        previous_output = None
        for parser in parser_names:
            try:
                soup = BeautifulSoup(self.markup, parser)
                if markup.startswith("<div>"):
                    # Extract the interesting part
                    output = soup.div
                else:
                    output = soup
            except Exception, e:
                output = "[EXCEPTION] %s" % str(e)
            self.results[parser] = output
            if previous_output is None:
                previous_output = output
            elif previous_output != output:
                uniform_results = False
        return uniform_results

    def dump(self):
        print "%s: %s" % ("Markup".rjust(13), self.markup.encode("utf8"))
        for parser, output in self.results.items():
            print "%s: %s" % (parser.rjust(13), output.encode("utf8"))

different_results = []
uniform_results = []

print "= Testing the following parsers: %s =" % ", ".join(parsers)
print

input_file = sys.stdin
if sys.stdin.isatty():
    for filename in [
        "demonstration_markup.txt",
        os.path.join("scripts", "demonstration_markup.txt")]:
        if os.path.exists(filename):
            input_file = open(filename)

for markup in input_file:
    demo = Demonstration(markup.decode("utf8").strip().replace("\\n", "\n"))
    is_uniform = demo.run_against(*parsers)
    if is_uniform:
        uniform_results.append(demo)
    else:
        different_results.append(demo)

print "== Markup that's handled the same in every parser =="
print
for demo in uniform_results:
    demo.dump()
    print
print "== Markup that's not handled the same in every parser =="
print
for demo in different_results:
    demo.dump()
    print
