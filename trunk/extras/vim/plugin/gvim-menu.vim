"
"      Filename:    t2t.vim
"   Description:    vim script to support txt2tag
"        Author:    Otávio Corrêa Cordeiro
"         Email:    cordeiro@exatas.unisinos.br
"          Date:    06 - October, 2004
"       Version:    0.2
"
"------------------------------------------------------------------------------------------
"    Copyright:  Copyright (C) 2004 Otávio Corrêa Cordeiro
"
"                This program is free software; you can redistribute it and/or modify
"                it under the terms of the GNU General Public License as published by
"                the Free Software Foundation; either version 2 of the License, or
"                (at your option) any later version.
"
"                This program is distributed in the hope that it will be useful,
"                but WITHOUT ANY WARRANTY; without even the implied warranty of
"                MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
"                GNU General Public License for more details.
"
"                You should have received a copy of the GNU General Public License
"                along with this program; if not, write to the Free Software
"                Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"------------------------------------------------------------------------------------------

amenu &txt2tags.Header                                 <Esc><Esc>aTitle<CR>Author<CR>%%date(%m/%d/%Y)<CR>

"amenu &txt2tags.Settings.Target
"amenu &txt2tags.Settings.Options(target)
"amenu &txt2tags.Settings.Include
"amenu &txt2tags.Settings.Style
amenu &txt2tags.Settings.Encoding\ (iso-8859-1)        <Esc><Esc>a%!encoding: iso-8859-1<CR>
imenu &txt2tags.Settings.Encoding\ (iso-8859-1)        <Esc><Esc>a%!encoding: iso-8859-1<CR>
"amenu &txt2tags.Settings.IncludeConf
"amenu &txt2tags.Settings.GuiColors
"amenu &txt2tags.Settings.ProProc

amenu &txt2tags.-SEP1-                                 :

amenu &txt2tags.Section                                <Esc><Esc>a=  =<Esc><Left>i
imenu &txt2tags.Section                                <Esc><Esc>a=  =<Esc><Left>i
vmenu &txt2tags.Section                                di=  =<Esc><Left>Pla
amenu &txt2tags.SubSection                             <Esc><Esc>a==  ==<Esc><Left><Left>i
imenu &txt2tags.SubSection                             <Esc><Esc>a==  ==<Esc><Left><Left>i
vmenu &txt2tags.SubSection                             di==  ==<Esc><Left><Left>Pla

amenu &txt2tags.-SEP2-                                 :

amenu &txt2tags.Beautifiers.Bold                       <Esc><Esc>a****<Esc><Left>i
vmenu &txt2tags.Beautifiers.Bold                       di****<Esc><Left>Pla
amenu &txt2tags.Beautifiers.Italic                     <Esc><Esc>a////<Esc><Left>i
vmenu &txt2tags.Beautifiers.Italic                     di////<Esc><Left>Pla
amenu &txt2tags.Beautifiers.Underline                  <Esc><Esc>a____<Esc><Left>i
vmenu &txt2tags.Beautifiers.Underline                  di____<Esc><Left>Pla
amenu &txt2tags.Beautifiers.Verbatim                   <Esc><Esc>a````<Esc><Left>i
vmenu &txt2tags.Beautifiers.Verbatim                   di````<Esc><Left>Pla

amenu &txt2tags.-SEP3-                                 :

amenu &txt2tags.Text\ Blocks.Quote                     <Esc><Esc>a<Tab>
imenu &txt2tags.Text\ Blocks.Quote                     <Esc><Esc>a<Tab>
amenu &txt2tags.Text\ Blocks.Verbatim                  <Esc><Esc>a```<Cr><Cr>```<Up>
imenu &txt2tags.Text\ Blocks.Verbatim                  <Esc><Esc>a```<Cr><Cr>```<Up>
vmenu &txt2tags.Text\ Blocks.Verbatim                  Di```<Cr>```<Cr><Esc>2kp
amenu &txt2tags.Text\ Blocks.List                      <Esc><Esc>i- 
imenu &txt2tags.Text\ Blocks.List                      <Esc><Esc>i- 
vmenu &txt2tags.Text\ Blocks.List                      :s/^/- /<Cr>
amenu &txt2tags.Text\ Blocks.Numbered\ List            <Esc><Esc>i+ 
imenu &txt2tags.Text\ Blocks.Numbered\ List            <Esc><Esc>i+ 
vmenu &txt2tags.Text\ Blocks.Numbered\ List            :s/^/\+ /<Cr>
amenu &txt2tags.Text\ Blocks.Definition\ List          <Esc><Esc>i: 
imenu &txt2tags.Text\ Blocks.Definition\ List          <Esc><Esc>i: 
vmenu &txt2tags.Text\ Blocks.Definition\ List          :s/^/: /<Cr>

amenu &txt2tags.-SEP4-                                 :

amenu &txt2tags.Separators.Thin                         <Esc><Esc>a--------------------------------------------------------<Cr>
imenu &txt2tags.Separators.Thin                         <Esc><Esc>a--------------------------------------------------------<Cr>
amenu &txt2tags.Separators.Large                        <Esc><Esc>a========================================================<Cr>
imenu &txt2tags.Separators.Large                        <Esc><Esc>a========================================================<Cr>

amenu &txt2tags.-SEP5-                                 :

amenu &txt2tags.Comments                               <Esc><Esc>a% 
imenu &txt2tags.Comments                               <Esc><Esc>a% 
