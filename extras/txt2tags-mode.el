;; Author: Leslie Harlley Watter


;; HOWTO INSTALL

;;
;; PT_BR  ( english users look below :D )
;;


;; 1) Crie/Copie este arquivo (txt2tags-mode.el) para o diretório ~/emacs/txt2tags/.
;; 2) Insira o seguinte código no final do seu ~/.emacs
;; ------
;; (add-to-list 'load-path "~/projetos/txt2tags/2.x/")
;; (setq auto-mode-alist (append (list
;; 	'("\\.t2t$" . t2t-mode)
;; 	)
;; 	(if (boundp 'auto-mode-alist) auto-mode-alist)
;; ))
;; (autoload  't2t-mode "txt2tags-mode" "Txt2tags Mode" t)
;; -----
;; E pronto, basta fechar e abrir novamente o emacs que ele irá carregar o txt2tags-mode automaticamente quando
;; um arquivo .t2t for aberto ;-)



;;
;; EN_US
;;

;; To install txt2tags-mode you just need to do a few steps:
;; 1) Copy this archieve (txt2tags-mode.el) to your ~/emacs/txt2tags directory. 
;; (If you don't have such a directory, you can create one just to organize your things)
;; 2) Add the following code to the end of your ~/.emacs
;; ------
;; (add-to-list 'load-path "~/projetos/txt2tags/2.x/")
;; (setq auto-mode-alist (append (list
;; 	'("\\.t2t$" . t2t-mode)
;; 	)
;; 	(if (boundp 'auto-mode-alist) auto-mode-alist)
;; ))
;; (autoload  't2t-mode "txt2tags-mode" "Txt2tags Mode" t)
;; -----
;; That's all. Close your emacs and reopen it. Emacs will parse and fontify all of .t2t files ;-)




;; TODO

;; Ajustar as regexps de tabelas
;; Ajustar a regexp da data para pegar %%date(%c) e variantes
;; rewrite the entire documentation.


(defvar t2t-mode-hook nil)
(defvar t2t-mode-map nil
  "Keymap for txt2tags major mode")

;; Now we're assigining a default keymap, if the user hasn't already defined one.

;; (if t2t-mode-map nil
;;   (setq t2t-mode-map (make-keymap)))



(defgroup t2t nil
  "txt2tags code editing commands for Emacs."
  :prefix "t2t-"
  :group 'languages)

(defcustom t2t-program 
  (cond 
   ((file-exists-p "/usr/local/bin/txt2tags") "/usr/local/bin/txt2tags")
   ((file-exists-p "/usr/bin/txt2tags") "/usr/bin/txt2tags")
   ((file-exists-p "/bin/txt2tags") "/bin/txt2tags")
;;   ((file-exists-p "/home/leslie/bin/bin/txt2tags") "/home/leslie/bin/bin/txt2tags")
   ((file-exists-p "~/projetos/txt2tags/programa/txt2tags") "~/projetos/txt2tags/programa/txt2tags")
   ( t "txt2tags")
   )
  "File name of the txt2tags executable."
  :type 'file
  :group 't2t)

(defcustom t2t-default-target "html"
  "Default target to txt2tags."
  :group 't2t)

;;; Fontes novas criadas com base na sugestão do kensanata do #emacs em irc.freenode.net

;; cria o novo grupo txt2tags-faces que é filho de txt2tags

(defgroup txt2tags-faces nil
  "txt2tags code editing commands for Emacs."
  :prefix "t2t-"
  :group 't2t)


;; data
(defface t2t-date-face '((t (:foreground "yellow" :background "black"))) 
  "Txt2Tags Date."  :group 'txt2tags-faces)

;; conf area
(defface t2t-config-face '((t (:foreground "yellow" :background "black"))) 
  "Txt2Tags Config Area."  :group 'txt2tags-faces)

;; conf area
(defface t2t-postproc-face '((t (:foreground "medium spring green" :background "black"))) 
  "Txt2Tags PostProc Area."  :group 'txt2tags-faces)


;; Verbatim
(defface t2t-verbatim-face '((t (:foreground "SpringGreen1" :background "black"))) 
  "Txt2Tags Verbatim."  :group 'txt2tags-faces)

;; http + e-mails

(defface t2t-internet-face '((t (:foreground "dark orchid" :background "black"))) 
  "Txt2Tags E-mail and Http." :group 'txt2tags-faces)

;; números

(defface t2t-numbers-face '((t (:foreground "plum1" :background "black"))) 
  "Txt2Tags Numbers." :group 'txt2tags-faces)

;; títulos de seções
(defface t2t-sections-face-5 '((t (:foreground "cyan" :background "black"))) 
  "Txt2Tags Section Titles." :group 'txt2tags-faces)

(defface t2t-sections-face-4 '((t (:foreground "cyan" :background "black"))) 
  "Txt2Tags Section Titles." :group 'txt2tags-faces)

(defface t2t-sections-face-3 '((t (:foreground "cyan" :background "black"))) 
  "Txt2Tags Section Titles." :group 'txt2tags-faces)

(defface t2t-sections-face-2 '((t (:foreground "cyan" :background "black"))) 
  "Txt2Tags Section Titles." :group 'txt2tags-faces)

(defface t2t-sections-face-1 '((t (:foreground "cyan" :background "black"))) 
  "Txt2Tags Section Titles." :group 'txt2tags-faces)


;; Comentários yellow4
(defface t2t-comments-face '((t (:foreground "yellow" :background "black"))) 
  "Txt2Tags Date." :group 'txt2tags-faces)

;; listas
(defface t2t-lists-face '((t (:foreground "dodger blue" :background "black"))) 
  "Txt2Tags Lists." :group 'txt2tags-faces)

;; quote
(defface t2t-quote-face '((t (:foreground "black" :background "yellow3"))) 
  "Txt2Tags Quote." :group 'txt2tags-faces)

;; raw
(defface t2t-raw-face '((t (:foreground "spring green" :background "black"))) 
  "Txt2Tags Raw." :group 'txt2tags-faces)

;; region
(defface t2t-region-face '((t (:foreground "green" :background "black"))) 
  "Txt2Tags Region." :group 'txt2tags-faces)

;; imagens
(defface t2t-images-face '((t (:foreground "SlateBlue4" :background "black"))) 
  "Txt2Tags Images." :group 'txt2tags-faces)

;; negrito
(defface t2t-bold-face '((t (:width extra-expanded :weight extra-bold :foreground "midnight blue" :background "black"))) 
  "Txt2Tags Bold." :group 'txt2tags-faces)

;; itálico
(defface t2t-italic-face '((t (:slant italic :foreground "SlateBlue2" :background "black"))) 
  "Txt2Tags Italic." :group 'txt2tags-faces)


;; negrito + itálico
(defface t2t-bold-italic-face '((t (:width extra-expanded :weight extra-bold :slant italic
			    :underline nil :foreground "medium slate blue" :background "black"))) 
  "Txt2Tags Bold Italic." :group 'txt2tags-faces)


;; tabelas
(defface t2t-tables-face '((t (:foreground "turquoise4" :background "black" :bold t))) 
  "Txt2Tags Tables." :group 'txt2tags-faces)


;; sublinhado
(defface t2t-underline-face '((t (:underline t :foreground "SlateBlue2" :background "black"))) 
  "Txt2Tags Underline." :group 'txt2tags-faces)

;; linha
(defface t2t-line-face '((t (:bold t :foreground "Blue2" :background "black"))) 
  "Txt2Tags line face." :group 'txt2tags-faces)

;; Fonte para mostrar o final de linha em branco em vermelho

(defface t2t-trailing-whitespace '((t (:bold t :foreground "Red" :background "black"))) 
  "Txt2Tags line face." :group 'txt2tags-faces)

;; Here, we append a definition to auto-mode-alist.
;; This tells emacs that when a buffer with a name ending with .t2t is opened, 
;; then t2t-mode should be started in that buffer. Some modes leave this step to the user.

(setq auto-mode-alist
	  (append
	   '(("\\.t2t\\'" . t2t-mode))
	   auto-mode-alist))


;; self comment
;;; Atenção !!! IMPORTANTE !!
;; NAO esquecer a aspa simples antes do nome da fonte   '("^%%.*" . --->'<----t2t-comments-face)
;; senão tem que declarar uma variável com o mesmo nome da fonte
;; Veja o comentário ao final deste modo



(defconst t2t-font-lock-keywords-0
  (list
   ;; raw - NEW
   '("[\"][\"]\\([^`]\\)+?[\"][\"]" . 't2t-verbatim-face)
   ;; Negrito - Bold
   '("[**][**][^ ][-/.,:?_  A-Za-zà-úÀ-Ú0-9]+?[^ ][**][**]" . 't2t-bold-face)
   ;; Itálico - Italic
   '("[/][/][^ ][-/.,:?_  A-Za-zà-úÀ-Ú0-9]+?[^ ][/][/]" . 't2t-italic-face) 
   ;; Sublinhado - Underline
   '("[_][_][^ ][-/.,:?_  A-Za-zà-úÀ-Ú0-9]+?[^ ][_][_]" . 't2t-underline-face)
   ;; verbatim 
   '("^``` .*$" . 't2t-verbatim-face)
   '("^```$" . 't2t-verbatim-face)
   ;; preformatado - prefformated  - verbatim
   '("``\\([^`]\\)+?``" . 't2t-verbatim-face)
   ;; linha horizontal - horizontal line - NEW
   '("-\\{19\\}-+" . 't2t-line-face)
   '("_\\{19\\}_+" . 't2t-line-face)
   '("=\\{19\\}=+" . 't2t-line-face)
   )
  "Minimal highlighting expressions for T2T mode")

(defconst t2t-font-lock-keywords-1
  (append t2t-font-lock-keywords-0
  (list
   ;; Data - Date
   '("%%date\\((%[mMdDyY][-/: ]%[mMdDyY][-/: ]%[mMdDyY])\\)?" . 't2t-date-face)
   '("%%date\\((%[mMdDyY][-/: ]%[mMdDyY])\\)" . 't2t-date-face)
   '("%%date[()%aAbBcdHImMdpSxXyY]+?" . 't2t-date-face)
   ;; Área de Configuração - Configuration area
   ;; casa %!target 
   '("%![-\"\<\>\'\{\}\\=;/.,:?_() A-Za-zà-úÀ-Ú0-9]+" . 't2t-config-face)
   ;; Postproc Area %%!postproc
   '("%%!postproc[-\"\<\>\'\{\}\\=;/.,:?_() A-Za-zà-úÀ-Ú0-9]+" . 't2t-postproc-face)
   ;; Comentários - Comments
   '("^%.*" . 't2t-comments-face)
   ;; Títulos de Seções não numerados - Unnumbered Section titles 
   '("=====[-/.,:?_() A-Za-zà-úÀ-Ú0-9\+=]+?=====$" . 't2t-sections-face-5) 
   '("====[-/.,:?_() A-Za-zà-úÀ-Ú0-9\+=]+?====$" . 't2t-sections-face-4) 
   '("===[-/.,:?_() A-Za-zà-úÀ-Ú0-9\+=]+?===$" . 't2t-sections-face-3) 
   '("==[-/.,:?_() A-Za-zà-úÀ-Ú0-9\+=]+?==$" . 't2t-sections-face-2) 
   '("=[-/.,:?_() A-Za-zà-úÀ-Ú0-9\+]+?=$" . 't2t-sections-face-1) 
   ;; Títulos de Seções não numerados com âncora - Unnumbered Section titles with anchors
   '("=====[-/.,:?_() A-Za-zà-úÀ-Ú0-9\+=]+?=====\[[-_A-Za-zà-úÀ-Ú0-9]+\]?$" . 't2t-sections-face-5) 
   '("====[-/.,:?_() A-Za-zà-úÀ-Ú0-9\+=]+?====\[[-_A-Za-zà-úÀ-Ú0-9]+\]?$" . 't2t-sections-face-4) 
   '("===[-/.,:?_() A-Za-zà-úÀ-Ú0-9\+=]+?===\[[-_A-Za-zà-úÀ-Ú0-9\]+\]?$" . 't2t-sections-face-3) 
   '("==[-/.,:?_() A-Za-zà-úÀ-Ú0-9\+=]+?==\[[-_A-Za-zà-úÀ-Ú0-9\]+\]?$" . 't2t-sections-face-2) 
   '("=[-/.,:?_() A-Za-zà-úÀ-Ú0-9]+?=\[[-_A-Za-zà-úÀ-Ú0-9]+\]?$" . 't2t-sections-face-1) 
   ;; Títulos de Seções numerados - Numbered Section titles 
   '("\\+\\+\\+\\+\\+[-/.,:?_() A-Za-zà-úÀ-Ú0-9=]+?\\+\\+\\+\\+\\+$" . 't2t-sections-face-5) 
   '("\\+\\+\\+\\+[-/.,:?_() A-Za-zà-úÀ-Ú0-9=]+?\\+\\+\\+\\+$" . 't2t-sections-face-4) 
   '("\\+\\+\\+[-/.,:?_() A-Za-zà-úÀ-Ú0-9=]+?\\+\\+\\+$" . 't2t-sections-face-3) 
   '("\\+\\+[-/.,:?_() A-Za-zà-úÀ-Ú0-9=]+?\\+\\+$" . 't2t-sections-face-2) 
   '("\\+[-/.,:?_() A-Za-zà-úÀ-Ú0-9=]+?\\+$" . 't2t-sections-face-1) 
   ;; Títulos de Seções numerados com âncora- Numbered Section titles with anchors
   '("\\+\\+\\+\\+\\+[-/.,:?_() A-Za-zà-úÀ-Ú0-9=]+?\\+\\+\\+\\+\\+\[[-_A-Za-zà-úÀ-Ú0-9]+\]?$" . 't2t-sections-face-5) 
   '("\\+\\+\\+\\+[-/.,:?_() A-Za-zà-úÀ-Ú0-9=]+?\\+\\+\\+\\+\[[-_A-Za-zà-úÀ-Ú0-9]+\]?$" . 't2t-sections-face-4) 
   '("\\+\\+\\+[-/.,:?_() A-Za-zà-úÀ-Ú0-9=]+?\\+\\+\\+\[[-_A-Za-zà-úÀ-Ú0-9]+\]?$" . 't2t-sections-face-3) 
   '("\\+\\+[-/.,:?_() A-Za-zà-úÀ-Ú0-9=]+?\\+\\+\[[-_A-Za-zà-úÀ-Ú0-9]+\]?$" . 't2t-sections-face-2) 
   '("\\+[-/.,:?_() A-Za-zà-úÀ-Ú0-9=]+?\\+\[[-_A-Za-zà-úÀ-Ú0-9]+\]?$" . 't2t-sections-face-1) 
   ))
  "Minimal highlighting expressions for T2T mode")


(defconst t2t-font-lock-keywords-2
  (append t2t-font-lock-keywords-1
		  (list
		   ;; image
		   '("\\[\\([-/.,:?_A-Za-zà-úÀ-Ú0-9]*\\)+\\]" . 't2t-images-face)
		   '("^ \\[\\([-/.,:?_A-Za-zà-úÀ-Ú0-9]*\\)+\\] $" . 't2t-images-face)
		   ;; quote - NEW
		   '("^\t+" . 't2t-quote-face)
		   '("^[ \t]*-" . 't2t-lists-face)
		   ;; colchetes - links 
		   '("\\[\\(.*?\\)\\]" . 't2t-internet-face) 
		   ;; páginas WEB - WEB pages
		   '("\\(http\\|https\\|ftp\\|telnet\\)://[A-Za-z]+[.:@][A-Za-z.:/@?#]+?[A-Za-z0-9=.:~!#$/@%&*?()+-_]+" . 't2t-internet-face)
		   '("\\(www\\|ftp\\)[0-9.]+?[A-Za-z]+[.:@][A-Za-z0-9=.:@~!#$%&/?*()+-_]+" . 't2t-internet-face)
		   ;; e-mails 
		   '("[A-Za-z0-9_.-]+@\\([A-Za-z0-9_-]+\.\\)+" . 't2t-internet-face)
		   ))
  "Additional Keywords to highlight in T2T mode")




(defconst t2t-font-lock-keywords-3
  (append t2t-font-lock-keywords-2
	  (list
	   ;; Tabela - Tables
	   ;; linha de titulo de tabela COM e SEM os pipes
	   ;; table title line  WITH and WITHOUT pipes
	   '("^ ?||\\( |\\| \\|\t\\|\\sw\\|[A-Za-zà-úÀ-Ú0-9]\\)+" . 't2t-tables-face)
	   ;; corpo da tabela - table body
	   '("^|\\(\\(\\s.\\|\\sw\\| \\|[A-Za-zà-úÀ-Ú0-9]\\)+\\( |\\)+\\)+" . 't2t-tables-face)
	   ;; corpo da tabela sem pipes - table body without pipes
;;	   '("^|\\(\\(\\( \\|\t\\)\\(\\s.\\|\\sw\\| \\|[à-úÀ-Ú0-9]\\)+\\)\\)+" . 't2t-tables-face)
	   ;; Listas -- (ainda nao vi como fazer com regioes inteiras)
	   ;; Lists
	   '("^[ \t]+- \\b" . 't2t-lists-face )
	   ;; definition list
	   '("^[ \t]*: \\b" . 't2t-lists-face )
	   ;; listas numeradas
	   '("^[ \t]*\\+ \\b" . 't2t-lists-face )
	   ;; numeros com cor também
	   '(" -?[0-9.]+" . 't2t-numbers-face)
	   )
	  )
  "Complete highlighting in T2T mode")


(defconst t2t-font-lock-keywords-4
  (append t2t-font-lock-keywords-3
	  (list
	   ;; regiões !!
	   '(txt2tags-region-lock-matcher
	     (0 't2t-region-face) 
	     (1 't2t-region-face))
	   )
	  )
  "Regions highlighting in T2T mode")


(defvar t2t-font-lock-keywords t2t-font-lock-keywords-4
  "Default highlighting expressions for Txt2Tags mode")


;; A syntax table tells Emacs how it should treat various tokens in your text for various functions,
;; including movement within the buffer and syntax highlighting. 
;; For example, how does Emacs know to move forward by one word (as used in the forward-word function)
;; The syntax table gives Emacs this kind of information. 
;; The syntax table is also used by the syntax highlighting package. 
;; It is for this reason that we want to modify the syntax table for t2t-mode.


;;  Original idea from font-latex-match-math-env command in font-latex.el.
;; retirado do emacs-wiki. Enquanto eu não tiver mais conhecimentos de lisp, fica como está
 (defun txt2tags-region-lock-matcher (limit)
   "
 ```
 This region will be highlighted
 ```
 " 
  ;; search for the begin of the first region
  (when (re-search-forward "^```$" limit t)
    (let ((beg (match-end 0)) end ; 1st Region
		  beg2 end2 ; 2nd Region
		) 
	  ;; search for end of region 1 and start of region 2
      (if (re-search-forward "^```$" limit t)
		  (progn
			(setq end (match-beginning 0)
				  beg2 (match-end 0))
			;; search for end of region 2
			(if (re-search-forward "^#end\n" limit t)
				(setq end2 (- (match-beginning 0) 1))
			  ;; no match -> length of region 2 = 0
			  (setq end2 beg2)))
		;; no match -> length of region 1 = 0
        (setq end (point)))
	  ;; save the regions
	  (store-match-data (list beg end beg2 end2))
      t)))



(defvar t2t-mode-syntax-table nil
  "Syntax table for t2t-mode.")

(defun t2t-create-syntax-table ()
  (if t2t-mode-syntax-table
      ()
    (setq t2t-mode-syntax-table (make-syntax-table))
	
	;; The first modification we make to the syntax table is to declare the 
	;; underscore character '_' as being a valid part of a word. 
	;; So now, a string like foo_bar will be treated as one word rather than two 
	;; (the default Emacs behavior). 
	
	(modify-syntax-entry ?_ "w" t2t-mode-syntax-table))

	;; %% inicia comentário 
;; 	(modify-syntax-entry ?/ ". 124b" t2t-mode-syntax-table)
;; 	(modify-syntax-entry ?* ". 23" t2t-mode-syntax-table)
;; 	(modify-syntax-entry ?\n "> b" t2t-mode-syntax-table))
  
  (set-syntax-table t2t-mode-syntax-table))


;; Here we define our entry function, give it a documentation string, make it interactive,
;;  and call our syntax table creation function.




;; menu

;; Nota: é NECESSARIO TER O t2t-mode-map definido como não nil para que funcione o menu

(defvar t2t-mode-map () "Keymap used in t2t-mode buffers.")

(when (not t2t-mode-map)
  (setq t2t-mode-map (make-sparse-keymap))
  (define-key t2t-mode-map [(control ?c) (control ?t) (control ?t)] 't2t-insert-normal-title)
  (define-key t2t-mode-map [(control ?c) (control ?t) (control ?n)] 't2t-insert-numbered-title)
  (define-key t2t-mode-map [(control ?c) (control ?f) (control ?b)] 't2t-insert-bold-face)
  (define-key t2t-mode-map [(control ?c) (control ?f) (control ?i)] 't2t-insert-italic-face)
  (define-key t2t-mode-map [(control ?c) (control ?f) (control ?u)] 't2t-insert-underlined-face)
  (define-key t2t-mode-map [(control ?c) (control ?f) (control ?m)] 't2t-insert-monospace-face)
  (define-key t2t-mode-map [(control ?c) (control ?b) (control ?c)] 't2t-insert-citation)
  (define-key t2t-mode-map [(control ?c) (control ?b) (control ?d)] 't2t-insert-definition-list)
  (define-key t2t-mode-map [(control ?c) (control ?b) (control ?l)] 't2t-insert-unumbered-list)
  (define-key t2t-mode-map [(control ?c) (control ?b) (control ?n)] 't2t-insert-numbered-list)
  (define-key t2t-mode-map [(control ?c) (control ?f) (control ?l)] 't2t-insert-formated-line)
  (define-key t2t-mode-map [(control ?c) (control ?f) (control ?a)] 't2t-insert-formated-area)
  (define-key t2t-mode-map [(control ?c) (control ?p) (control ?l)] 't2t-insert-protected-line)
  (define-key t2t-mode-map [(control ?c) (control ?p) (control ?a)] 't2t-insert-protected-area)
  (define-key t2t-mode-map [(control ?c) (control ?p) (control ?t)] 't2t-insert-protected-text)
  (define-key t2t-mode-map [(control ?c) (control ?o) (control ?s)] 't2t-insert-separation-line)
  (define-key t2t-mode-map [(control ?c) (control ?o) (control ?d)] 't2t-insert-emphasize-line)
  (define-key t2t-mode-map [(control ?c) (control ?l)]              't2t-insert-link)
  (define-key t2t-mode-map [(control ?c) (control ?i)]              't2t-insert-image)
  (define-key t2t-mode-map [(control ?c) (control ?d)]              't2t-insert-date)
  (define-key t2t-mode-map [(control ?c) (control ?c)]              't2t-insert-comments)
)


;; esse if é responsável por verificar a linguagem do sistema

(if (string= (getenv "LANG") "pt_BR")
;; ok, the user is using pt_BR language
(easy-menu-define t2t-mode-menu t2t-mode-map
  "'Txt2Tags-mode' menu"
  '("T2T"
    ("Título" 
     ["Normal"       (t2t-insert-normal-title)      :keys "C-c C-t C-t"]
     ["Numerado"     (t2t-insert-numbered-title)    :keys "C-c C-t C-n"]
     )
    ("Embelezadores"
     ["Negrito"      (t2t-insert-bold-face)         :keys "C-c C-f C-b"]
     ["Itálico"      (t2t-insert-italic-face)       :keys "C-c C-f C-i"]

     ["Sublinhado"   (t2t-insert-underlined-face)   :keys "C-c C-f C-u"]
     ["Monoespaçado" (t2t-insert-monospace-face)    :keys "C-c C-f C-m"]
     ;; (progn (save-excursion (goto-char (mark)) (insert "''")) (insert "''"))
     )
    ("Blocos de Texto"
     ["Citação"             (t2t-insert-citation)        :keys "C-c C-b C-c"]
     ["Lista"               (t2t-insert-unumbered-list)  :keys "C-c C-b C-l"]
     ["Lista Numerada"      (t2t-insert-numbered-list)   :keys "C-c C-b C-n"]
     ["Lista de Definição"  (t2t-insert-definition-list) :keys "C-c C-b C-d"]
     )
    ("Texto Formatado"
     ["Linha Formatada"     (t2t-insert-formated-line)   :keys "C-c C-f C-l"]
     ["Área Formatada"      (t2t-insert-formated-area)   :keys "C-c C-f C-a"]
     )
    ("Texto Protegido"
     ["Linha Protegida"     (t2t-insert-protected-line) :keys "C-c C-p C-l"]
     ;; (progn (save-excursion (goto-char (mark)) (beginning-of-line)) (insert "\n\"\"\" ")) 
     ["Área Protegida"      (t2t-insert-protected-area) :keys "C-c C-p C-a"]
     ;; (progn (save-excursion (goto-char (mark)) (insert "\n\"\"\"\n")) (insert "\n\"\"\"\n")) 
     ["Texto Protegido"     (t2t-insert-protected-text) :keys "C-c C-p C-t"]
     ;; (progn (save-excursion (goto-char (mark)) (insert "\"\"")) (insert "\"\"")) 
     ;;      ["Tabela" 
     ;;       () t]
     )
    ("Outros"
     ["Linha de Separação"   (t2t-insert-separation-line) :keys "C-c C-o C-s"]
     ;; (progn (save-excursion (goto-char (mark)) (beginning-of-line)) (insert "\n----------------------")) 
     ["Linha Destacada"      (t2t-insert-emphasize-line)  :keys "C-c C-o C-d"]
     ;; (progn (save-excursion (goto-char (mark)) (beginning-of-line)) (insert "\n======================"))
     )
    ("--")
	["Links"                (t2t-insert-link)            :keys "C-c C-l"]
	["Imagem"               (t2t-insert-image)           :keys "C-c C-i"]
	["Data Atual"           (t2t-insert-date)            :keys "C-c C-d"]
    ["Comentário"           (t2t-insert-comments)        :keys "C-c C-c"]
    ;;     (progn (save-excursion (goto-char (mark)) (beginning-of-line) (insert ?% " ")))
    )
  )
;; other language; try english as default
(easy-menu-define t2t-mode-menu t2t-mode-map
  "'Txt2Tags-mode' menu"
  '("T2T"
    ("Title" 
     ["Ununmbered"       (t2t-insert-normal-title)      :keys "C-c C-t C-t"]
     ["Numbered"     (t2t-insert-numbered-title)    :keys "C-c C-t C-n"]
     )
    ("Font Beautifiers"
     ["Bold"      (t2t-insert-bold-face)         :keys "C-c C-f C-b"]
     ["Italic"      (t2t-insert-italic-face)       :keys "C-c C-f C-i"]

     ["Underline"   (t2t-insert-underlined-face)   :keys "C-c C-f C-u"]
     ["Monospaced" (t2t-insert-monospace-face)    :keys "C-c C-f C-m"]
     ;; (progn (save-excursion (goto-char (mark)) (insert "''")) (insert "''"))
     )
    ("Text Blocks"
     ["Citation"             (t2t-insert-citation)        :keys "C-c C-b C-c"]
     ["List"               (t2t-insert-unumbered-list)  :keys "C-c C-b C-l"]
     ["Numbered List"      (t2t-insert-numbered-list)   :keys "C-c C-b C-n"]
     ["Definition List"  (t2t-insert-definition-list) :keys "C-c C-b C-d"]
     )
    ("Verbatim"
     ["Verbatim Line"     (t2t-insert-formated-line)   :keys "C-c C-f C-l"]
     ["Verbatim Area"      (t2t-insert-formated-area)   :keys "C-c C-f C-a"]
     )
    ("RAW"
     ["Raw line"     (t2t-insert-protected-line) :keys "C-c C-p C-l"]
     ;; (progn (save-excursion (goto-char (mark)) (beginning-of-line)) (insert "\n\"\"\" ")) 
     ["Raw area"      (t2t-insert-protected-area) :keys "C-c C-p C-a"]
     ;; (progn (save-excursion (goto-char (mark)) (insert "\n\"\"\"\n")) (insert "\n\"\"\"\n")) 
     ["RAW Text"     (t2t-insert-protected-text) :keys "C-c C-p C-t"]
     ;; (progn (save-excursion (goto-char (mark)) (insert "\"\"")) (insert "\"\"")) 
     ;;      ["Tabela" 
     ;;       () t]
     )
    ("Others"
     ["Horizontal Separator Line"   (t2t-insert-separation-line) :keys "C-c C-o C-s"]
     ;; (progn (save-excursion (goto-char (mark)) (beginning-of-line)) (insert "\n----------------------")) 
     ["Horizontal Bold Line"      (t2t-insert-emphasize-line)  :keys "C-c C-o C-d"]
     ;; (progn (save-excursion (goto-char (mark)) (beginning-of-line)) (insert "\n======================"))
     )
    ("--")
	["Links"              (t2t-insert-link)            :keys "C-c C-l"]
	["Image"              (t2t-insert-image)           :keys "C-c C-i"]
	["Date"               (t2t-insert-date)            :keys "C-c C-d"]
    ["Comments"           (t2t-insert-comments)        :keys "C-c C-c"]
    ;;     (progn (save-excursion (goto-char (mark)) (beginning-of-line) (insert ?% " ")))
    )
  )

) ;; ends if language   




;; titles

(defun t2t-insert-normal-title ()
  (interactive)
  (save-excursion (goto-char (point)) (beginning-of-line)
		  (insert "\n= "))
  (end-of-line)
  (insert " ="))


(defun t2t-insert-numbered-title ()
  (interactive)
  (save-excursion (goto-char (point)) (beginning-of-line)
		  (insert "\n+ "))
  (end-of-line)
  (insert " +"))

;; faces

(defun t2t-insert-bold-face ()
  (interactive)
  (save-excursion (goto-char (region-beginning))
		  (insert "**"))
  (insert "**"))


(defun t2t-insert-italic-face ()
  (interactive)
  (save-excursion (goto-char (region-beginning))
		  (insert "//"))
  (insert "//"))


(defun t2t-insert-underlined-face ()
  (interactive)
  (save-excursion (goto-char (region-beginning))
		  (insert "__"))
  (insert "__"))

(defun t2t-insert-monospace-face ()
  (interactive)
  (save-excursion (goto-char (region-beginning))
		  (insert "''"))
  (insert "''"))

;; lists

(defun t2t-insert-citation ()
  (interactive)
  (setq citat (read-string "Texto: "))
  (unless (equal citat "")
  (insert (format "\n\t" citat ))))

(defun t2t-insert-definition-list ()
  (interactive)
  (setq descr (read-string "Item: "))
  (unless (equal descr "")
  (insert (format "\n : %s \n" descr ))))


(defun t2t-insert-unumbered-list ()
  (interactive)
  (setq unumberedlist (read-string "Item: "))
  (unless (equal unumberedlist "")
    (insert (format "\n - %s" unumberedlist))))


(defun t2t-insert-numbered-list ()
  (interactive)
  (setq numberedlist (read-string "Item: "))
  (unless (equal numberedlist "")
    (insert (format "\n + %s" numberedlist))))


;; Texto formatado
(defun t2t-insert-formated-line ()
  (interactive)
  (save-excursion (goto-char (region-beginning)) (end-of-line)) (insert "\n''' "))


(defun t2t-insert-formated-area ()
  (interactive)
  (save-excursion (goto-char (region-beginning)) (insert "\n'''\n")) (insert "\n'''\n"))



;; texto protegido

(defun t2t-insert-protected-line ()
  (interactive)
  (save-excursion (goto-char (region-beginning)) (beginning-of-line) (insert "\"\"\" ")))

(defun t2t-insert-protected-area ()
  (interactive)
  (save-excursion (goto-char (region-beginning)) (insert "\n\"\"\"\n"))
  (insert "\n\"\"\"\n"))

(defun t2t-insert-protected-text ()
  (interactive)
  (save-excursion (goto-char (region-beginning)) (insert "\"\"")) (insert "\"\""))



(defun t2t-insert-separation-line ()
  (interactive)
  (save-excursion 
    (goto-line (point)) 
    (end-of-line) 
    (insert "\n----------------------")))


(defun t2t-insert-emphasize-line ()
  (interactive)
  (save-excursion 
    (goto-line (point)) 
    (end-of-line) 
    (insert "\n======================")))


(defun t2t-insert-link ()
  (interactive)
  (setq linkname (read-string "Nome: "))
  (unless (equal linkname "")
    (setq urllink (read-string "Link: "))
    (unless (equal urllink "")
    (insert (format "[%s %s]" linkname urllink)))))

(defun t2t-insert-image ()
  (interactive)
  (setq fileplusextension (read-string "Arquivo.Ext: "))
  (unless (equal fileplusextension "")
    (insert (format "[%s]" fileplusextension))))


(defun t2t-insert-date ()
  (interactive)
  (save-excursion (goto-char (point)) (beginning-of-line) (insert ?% ?% "date\(\)")))


(defun t2t-insert-comments ()
  (interactive)
  (save-excursion (goto-char (point)) (beginning-of-line) (insert ?% " ")))

(defun t2t-mode ()
  "Major mode for editing Txt2Tags files"
  (interactive)
  (kill-all-local-variables)
  (t2t-create-syntax-table)
  (make-local-variable 'font-lock-defaults)
  (setq font-lock-defaults
		'(t2t-font-lock-keywords))

;; faz com que o final de linha seja mostrado em vermelho

  (add-hook 't2t-mode-hook
	    (lambda ()
	      (set (make-local-variable 'show-trailing-whitespace)
			   t )))

;; Muda a variável compile-command para txt2tags arquivo.t2t
  (add-hook 't2t-mode-hook
	    (lambda ()
	      (set (make-local-variable 'compile-command)
		   (let ((file (file-name-nondirectory buffer-file-name)))
		     (concat t2t-program " -t " t2t-default-target " " file)))))
  
;; Ativa por padrão o syntax higlight
  (add-hook 't2t-mode-hook 'turn-on-font-lock)
;; ativa o mapa e menu
  (use-local-map t2t-mode-map)
  (easy-menu-add t2t-mode-menu)
;; major-mode
  (setq major-mode 't2t-mode)
  (setq mode-name "T2T")
  (run-hooks 't2t-mode-hook))

(provide 't2t-mode)

