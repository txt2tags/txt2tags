# aa.py
# The ASCII Art library for Python
#
# Copyright 2008-2015 Florent Gallaire <fgallaire@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

import re
import textwrap
import unicodedata


QA = """\
       ________
   /#**TXT2TAGS**#\\
 /#####/      \####CC\\
/###/            \#BY#|
^-^               |NC#|
                  /SA#|
               /#####/
            /#####/
          /####/
         /###/
        |###|
        |###|
         \o/

         ___
        F2.7G
         (C)\
""".split('\n')


def line(char, width):
    return char * width


def under(txt, char, width, over):
    ret = []
    if over:
        ret.append(line(char, lencjk(txt)))
    for lin in wrap(txt, width, False):
        ret.extend([lin, line(char, lencjk(lin))])
    return ret


def quote(txt, char, width, depth, web):
    if char in '123456789':
        prefix = int(char) * depth * ' '
        wrap_depth = width - int(char) * depth
    else:
        prefix = char * depth + ' '
        wrap_depth = width - depth - 1
    wrap_txt = wrap(txt, wrap_depth, web)
    block_txt = [prefix + line for line in wrap_txt]
    return block_txt


def box(txt, chars, width, centred=True, web=False, slides=False):
    wrap_txt = []
    char_side = ''
    if slides:
        width = width - 2
        char_side = ' '
    for lin in txt:
        wrap_txt.extend(wrap(lin, width - 4, web))
    len_cjk = max([lencjk(lin, web) for lin in wrap_txt])
    tline_box = char_side + center(chars['tlcorner'] + chars['border'] * (len_cjk + 2) + chars['trcorner'], width) + char_side
    bline_box = char_side + center(chars['blcorner'] + chars['border'] * (len_cjk + 2) + chars['brcorner'], width) + char_side
    line_txt = []
    for lin in wrap_txt:
        if centred:
            line_txt.append(char_side + center(chars['side'] + ' ' + center(lin, len_cjk, web) + ' ' + chars['side'], width, web) + char_side)
        else:
            line_txt.append(char_side + center(chars['side'] + ' ' + lin + ' ' * (len_cjk - lencjk(lin, web) + 1) + chars['side'], width, web) + char_side)
    return [tline_box] + line_txt + [bline_box]


def header(header_data, chars, width, height, web, slides, printing):
    h = [header_data[v] for v in header_data if v.startswith("HEADER") and header_data[v]]
    n_h = len(h)
    height_box = sum([len(box([header], chars, width, slides=slides)) for header in h])
    if not n_h:
        return []
    if not slides:
        n, end = 2, 0
    else:
        x = height - 2 - height_box
        n = x / (n_h + 1)
        end = x % (n_h + 1)
    header = [line(chars['bar2'], width)]
    header.extend([''] * n)
    for h in 'HEADER1', 'HEADER2', 'HEADER3':
        if header_data[h]:
            header.extend(box([header_data[h]], chars, width, slides=slides))
            header.extend([''] * n)
    header.extend([''] * end)
    header.append(line(chars['bar2'], width))
    if slides:
        if web:
            header = ['<section><pre>' + header[0]] + header[1:-1] + [header[-1] + '</pre></section>']
        elif printing:
            header = header[:-1] + [header[-1] + '']
    if not slides or printing:
        header = [''] + header
    return header


def slide(title, char, width, web):
    res = [line(char, width)]
    res.append('')
    res.append(center(title, width)[:width])
    res.append('')
    res.append(line(char, width))
    if web:
        res = ['<section><pre>' + res[0]] + res[1:]
    return res


def table(data, chars, width, borders, h_header, v_header, align, spread, web):
    n = max([len(lin[0]) for lin in data])
    data3 = []
    for lin in data:
        if  max(lin[1]) == 1:
            data3.append(lin[0])
        else:
            newline = []
            for i, el in enumerate(lin[0]):
                if lin[1][i] == 1:
                    newline.append(el)
                else:
                    newline.extend(lin[1][i] * [''])
            data3.append(newline)
    tab = []
    for i in range(n):
        tab.append([lin[i] for lin in data3])
    if web:
        length = [max([lencjk(re.sub('<a.*">|</a>', '', el)) for el in lin]) for lin in tab]
    else:
        length = [max([lencjk(el) for el in lin]) for lin in tab]
    if spread:
        data[0][0] = [data[0][0][i].center(length[i]) for i in range(n)]
    tcross, border, bcross, lcross, side, rcross, tlcorner, trcorner, cross, blcorner, brcorner, tvhead, vhead, vheadcross, bvhead ,headerscross, hhead, hheadcross, lhhead, rhhead= chars['tcross'], chars['border'], chars['bcross'], chars['lcross'], chars['side'], chars['rcross'], chars['tlcorner'], chars['trcorner'], chars['cross'], chars['blcorner'], chars['brcorner'], chars['tvhead'], chars['vhead'], chars['vheadcross'], chars['bvhead'], chars['headerscross'], chars['hhead'], chars['hheadcross'], chars['lhhead'], chars['rhhead']
    if not v_header:
        tvhead, bvhead = tcross, bcross
        if borders:
            vheadcross = cross
            if h_header:
                headerscross = hheadcross
    if not borders:
        hhead, hheadcross, lhhead, rhhead, headerscross = border, cross, lcross, rcross, vheadcross
        if h_header and not v_header:
                headerscross = cross
    if v_header and not h_header:
        headerscross = vheadcross
    len0 = length[0] + 2
    res = lcross + len0 * border + vheadcross
    resh = lhhead + len0 * hhead + headerscross
    rest = tlcorner + len0 * border + tvhead
    resb = blcorner + len0 * border + bvhead
    for i in range(1, n):
        res = res + (length[i] + 2) * border + cross
        resh = resh + (length[i] + 2) * hhead + hheadcross
        rest = rest + (length[i] + 2) * border + tcross
        resb = resb + (length[i] + 2) * border + bcross
    res = res[:-1] + rcross
    resh = resh[:-1] + rhhead
    rest = rest[:-1] + trcorner
    resb = resb[:-1] + brcorner
    ret = []
    for i, lin in enumerate(data):
        aff = side
        if i == 1 and h_header:
            ret.append(resh)
        elif i == 0:
            ret.append(rest)
        elif borders:
            ret.append(res)
        for j, el in enumerate(lin[0]):
            if web:
                aff = aff + " " + el + (sum(length[j:(j + lin[1][j])]) + lin[1][j] * 3 - lencjk(re.sub('<a.*">|</a>', '',el)) - 2) * " " + side
            else:
                aff = aff + " " + el + (sum(length[j:(j + lin[1][j])]) + lin[1][j] * 3 - lencjk(el) - 2) * " " + side
            if j == 0 and v_header:
                aff = aff[:-1] + vhead
        ret.append(aff)
    ret.append(resb)
    if align == 'Left':
        ret = [' ' * 2  + lin for lin in ret]
    elif align == 'Center' and not (web and spread):
        ret = [center(lin, width) for lin in ret]
    return ret


def image(image):
    art_table = '#$!;:,. '
    art_image = []
    for lin in image:
        art_line = ''
        for pixel in lin:
            art_line = art_line + art_table[pixel/32]
        art_image.append(art_line)
    return art_image


def wrap(txt, width, web):
    twcjk = TextWrapperCJK(width=width)
    if not web:
        return twcjk.wrap(txt)
    txt = re.split('(<a href=.*?>)|(</a>)|(<img src=.*?>)', txt)
    lin, length, ret = '', 0, []
    for el in txt:
        if el:
            if el[0] != '<':
                if len(el) > width:
                    lin = lin + el
                    multi = twcjk.wrap(lin)
                    ret.extend(multi[:-1])
                    lin = multi[-1]
                elif length + len(el) <= width:
                    length = length + len(el)
                    lin = lin + el
                else:
                    ret.append(lin)
                    lin, length = el, len(el)
            else:
                    lin = lin + el
    ret.append(lin)
    return ret


def lencjk(txt, web=False):
    if web:
        txt = re.sub('(<a href=.*?>)|(</a>)|(<img src=.*?>)', '', txt)
    if isinstance(txt, str):
        return len(txt)
    l = 0
    for char in txt:
        if unicodedata.east_asian_width(unicode(char)) in ('F', 'W'):
            l = l + 2
        else:
            l = l + 1
    return l


def slicecjk(txt, space_left):
    if isinstance(txt, str):
        return txt[:space_left], txt[space_left:]
    i = 1
    while lencjk(txt[:i]) <= space_left:
        # <= and index i-1
        # to catch the last double length char of odd line
        i = i + 1
    return txt[:i-1], txt[i-1:]


class TextWrapperCJK(textwrap.TextWrapper):
    # CJK fix for the Greg Ward textwrap lib. 
    def _handle_long_word(self, reversed_chunks, cur_line, cur_len, width):
        if width < 1:
            space_left = 1
        else:
            space_left = width - cur_len
        if self.break_long_words:
            chunk_start, chunk_end = slicecjk(reversed_chunks[-1], space_left)
            cur_line.append(chunk_start)
            reversed_chunks[-1] = chunk_end
        elif not cur_line:
            cur_line.append(reversed_chunks.pop())
    def _wrap_chunks(self, chunks):
        lines = []
        if self.width <= 0:
            raise ValueError("invalid width %r (must be > 0)" % self.width)
        chunks.reverse()
        while chunks:
            cur_line = []
            cur_len = 0
            if lines:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent
            width = self.width - len(indent)
            if self.drop_whitespace and chunks[-1].strip() == '' and lines:
                del chunks[-1]
            while chunks:
                l = lencjk(chunks[-1])
                if cur_len + l <= width:
                    cur_line.append(chunks.pop())
                    cur_len += l
                else:
                    break
            if chunks and lencjk(chunks[-1]) > width:
                self._handle_long_word(chunks, cur_line, cur_len, width)
            if self.drop_whitespace and cur_line and cur_line[-1].strip() == '':
                del cur_line[-1]
            if cur_line:
                lines.append(indent + ''.join(cur_line))
        return lines


def center(txt, width, web=False):
    n_before = (width - lencjk(txt, web)) / 2
    n_after = width - lencjk(txt, web) - n_before
    return ' ' * n_before + txt + ' ' * n_after
