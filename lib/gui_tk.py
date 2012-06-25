##############################################################################
################################### GUI ######################################
##############################################################################
#
# Tk help: http://python.org/topics/tkinter/
#    Tuto: http://ibiblio.org/obp/py4fun/gui/tkPhone.html
#          /usr/lib/python*/lib-tk/Tkinter.py
#
# grid table : row=0, column=0, columnspan=2, rowspan=2
# grid align : sticky='n,s,e,w' (North, South, East, West)
# pack place : side='top,bottom,right,left'
# pack fill  : fill='x,y,both,none', expand=1
# pack align : anchor='n,s,e,w' (North, South, East, West)
# padding    : padx=10, pady=10, ipadx=10, ipady=10 (internal)
# checkbox   : offvalue is return if the _user_ deselected the box
# label align: justify=left,right,center

import sys
import Tkinter
from tkFileDialog import askopenfilename
from tkMessageBox import showinfo, showwarning, showerror


class Gui:
    "Graphical Tk Interface"
    def __init__(self, my_name, my_version, my_url, STDOUT, TARGETS, TARGET_NAMES, conf={}):
        self.my_name = my_name
        self.my_version = my_version
        self.my_url = my_url
        self.STDOUT = STDOUT
        self.TARGETS = TARGETS
        self.TARGET_NAMES = TARGET_NAMES
        self.root = Tkinter.Tk()    # mother window, come to butthead
        self.root.title(my_name)    # window title bar text
        self.window = self.root     # variable "focus" for inclusion
        self.row = 0                # row count for grid()

        self.action_length = 150    # left column length (pixel)
        self.frame_margin  = 10     # frame margin size  (pixel)
        self.frame_border  = 6      # frame border size  (pixel)

        # The default Gui colors, can be changed by %!guicolors
        self.dft_gui_colors = ['#6c6', 'white', '#cf9', '#030']
        self.gui_colors = []
        self.bg1 = self.fg1 = self.bg2 = self.fg2 = ''

        # On Tk, vars need to be set/get using setvar()/get()
        self.infile  = self.setvar('')
        self.target  = self.setvar('')
        self.target_name = self.setvar('')

        # The checks appearance order
        self.checks = [
            'headers', 'enum-title', 'toc', 'mask-email', 'toc-only', 'stdout'
        ]

        # Creating variables for all checks
        for check in self.checks:
            setattr(self, 'f_' + check, self.setvar(''))

        # Load RC config
        self.conf = {}
        if conf:
            self.load_config(conf)

    def load_config(self, conf):
        self.conf = conf
        self.gui_colors = conf.get('guicolors') or self.dft_gui_colors
        self.bg1, self.fg1, self.bg2, self.fg2 = self.gui_colors
        self.root.config(bd=15, bg=self.bg1)

    ### Config as dic for python 1.5 compat (**opts don't work :( )
    def entry(self, **opts):
        return Tkinter.Entry(self.window, opts)

    def label(self, txt='', bg=None, **opts):
        opts.update({'text': txt, 'bg': bg or self.bg1})
        return Tkinter.Label(self.window, opts)

    def button(self, name, cmd, **opts):
        opts.update({'text': name, 'command': cmd})
        return Tkinter.Button(self.window, opts)

    def check(self, name, checked=0, **opts):
        bg, fg = self.bg2, self.fg2
        opts.update({
            'text': name,
            'onvalue': 1,
            'offvalue': 0,
            'activeforeground': fg,
            'activebackground': bg,
            'highlightbackground': bg,
            'fg': fg,
            'bg': bg,
            'anchor': 'w'
        })
        chk = Tkinter.Checkbutton(self.window, opts)
        if checked:
            chk.select()
        chk.grid(columnspan=2, sticky='w', padx=0)

    def menu(self, sel, items):
        return apply(Tkinter.OptionMenu, (self.window, sel) + tuple(items))

    # Handy auxiliary functions
    def action(self, txt):
        self.label(
            txt,
            fg=self.fg1,
            bg=self.bg1,
            wraplength=self.action_length).grid(column=0, row=self.row)

    def frame_open(self):
        self.window = Tkinter.Frame(
            self.root,
            bg=self.bg2,
            borderwidth=self.frame_border)

    def frame_close(self):
        self.window.grid(
            column=1,
            row=self.row,
            sticky='w',
            padx=self.frame_margin)
        self.window = self.root
        self.label('').grid()
        self.row += 2   # update row count

    def target_name2key(self):
        name = self.target_name.get()
        target = filter(lambda x: self.TARGET_NAMES[x] == name, self.TARGETS)
        try   :
            key = target[0]
        except:
            key = ''
        self.target = self.setvar(key)

    def target_key2name(self):
        key = self.target.get()
        name = self.TARGET_NAMES.get(key) or key
        self.target_name = self.setvar(name)

    def exit(self):
        self.root.destroy()

    def setvar(self, val):
        z = Tkinter.StringVar()
        z.set(val)
        return z

    def askfile(self):
        ftypes = [('txt2tags files', ('*.t2t', '*.txt')), ('All files', '*')]
        newfile = askopenfilename(filetypes=ftypes)
        if newfile:
            self.infile.set(newfile)
            newconf = process_source_file(newfile)[0]
            newconf = ConfigMaster().sanity(newconf, gui=1)
            # Restate all checkboxes after file selection
            #TODO how to make a refresh without killing it?
            self.root.destroy()
            self.__init__(newconf)
            self.mainwindow()

    def scrollwindow(self, txt='no text!', title=''):
        # Create components
        win    = Tkinter.Toplevel()
        win.title(title)
        frame  = Tkinter.Frame(win)
        scroll = Tkinter.Scrollbar(frame)
        text   = Tkinter.Text(frame, yscrollcommand=scroll.set)
        button = Tkinter.Button(win)
        # Config
        text.insert(Tkinter.END, '\n'.join(txt))
        scroll.config(command=text.yview)
        button.config(text='Close', command=win.destroy)
        button.focus_set()
        # Packing
        text.pack(side='left', fill='both', expand=1)
        scroll.pack(side='right', fill='y')
        frame.pack(fill='both', expand=1)
        button.pack(ipadx=30)

    def runprogram(self):
        global CMDLINE_RAW
        # Prepare
        self.target_name2key()
        infile, target = self.infile.get(), self.target.get()
        # Sanity
        if not target:
            showwarning(self.my_name, "You must select a target type!")
            return
        if not infile:
            showwarning(self.my_name, "You must provide the source file location!")
            return
        # Compose cmdline
        guiflags = []
        real_cmdline_conf = ConfigMaster(CMDLINE_RAW).parse()
        if 'infile' in real_cmdline_conf:
            del real_cmdline_conf['infile']
        if 'target' in real_cmdline_conf:
            del real_cmdline_conf['target']
        real_cmdline = CommandLine().compose_cmdline(real_cmdline_conf)
        default_outfile = ConfigMaster().get_outfile_name(
            {'sourcefile': infile, 'outfile': '', 'target': target})
        for opt in self.checks:
            val = int(getattr(self, 'f_%s' % opt).get() or "0")
            if opt == 'stdout':
                opt = 'outfile'
            on_config  = self.conf.get(opt) or 0
            on_cmdline = real_cmdline_conf.get(opt) or 0
            if opt == 'outfile':
                if on_config  == STDOUT:
                    on_config = 1
                else:
                    on_config = 0
                if on_cmdline == STDOUT:
                    on_cmdline = 1
                else:
                    on_cmdline = 0
            if val != on_config or (
              val == on_config == on_cmdline and
              opt in real_cmdline_conf):
                if val:
                    # Was not set, but user selected on GUI
                    Debug("user turned  ON: %s" % opt)
                    if opt == 'outfile':
                        opt = '-o-'
                    else:
                        opt = '--%s' % opt
                else:
                    # Was set, but user deselected on GUI
                    Debug("user turned OFF: %s" % opt)
                    if opt == 'outfile':
                        opt = "-o%s" % default_outfile
                    else:
                        opt = '--no-%s' % opt
                guiflags.append(opt)
        cmdline = [slef.my_name, '-t', target] + real_cmdline + guiflags + [infile]
        Debug('Gui/Tk cmdline: %s' % cmdline, 5)
        # Run!
        cmdline_raw_orig = CMDLINE_RAW
        try:
            # Fake the GUI cmdline as the real one, and parse file
            CMDLINE_RAW = CommandLine().get_raw_config(cmdline[1:])
            data = process_source_file(infile)
            # On GUI, convert_* returns the data, not finish_him()
            outlist, config = convert_this_files([data])
            # On GUI and STDOUT, finish_him() returns the data
            result = finish_him(outlist, config)
            # Show outlist in s a nice new window
            if result:
                outlist, config = result
                title = '%s: %s converted to %s' % (
                    self.my_name,
                    os.path.basename(infile),
                    config['target'].upper())
                self.scrollwindow(outlist, title)
            # Show the "file saved" message
            else:
                msg = "%s\n\n  %s\n%s\n\n  %s\n%s" % (
                    'Conversion done!',
                    'FROM:', infile,
                    'TO:', config['outfile'])
                showinfo(self.my_name, msg)
        except error:         # common error (windowed), not quit
            pass
        except:               # fatal error (windowed and printed)
            errormsg = getUnknownErrorMessage()
            print errormsg
            showerror('%s FATAL ERROR!' % self.my_name, errormsg)
            self.exit(1)
        CMDLINE_RAW = cmdline_raw_orig

    def mainwindow(self):
        self.infile.set(self.conf.get('sourcefile') or '')
        self.target.set(self.conf.get('target') or '-- select one --')
        outfile = self.conf.get('outfile')
        if outfile == self.STDOUT:                  # map -o-
            self.conf['stdout'] = 1
        if self.conf.get('headers') == None:
            self.conf['headers'] = 1       # map default

        action1 = "Enter the source file location:"
        action2 = "Choose the target document type:"
        action3 = "Some options you may check:"
        action4 = "Some extra options:"
        checks_txt = {
            'headers'   : "Include headers on output",
            'enum-title': "Number titles (1, 1.1, 1.1.1, etc)",
            'toc'       : "Do TOC also (Table of Contents)",
            'mask-email': "Hide e-mails from SPAM robots",

            'toc-only'  : "Just do TOC, nothing more",
            'stdout'    : "Dump to screen (Don't save target file)"
        }
        targets_menu = map(lambda x: self.TARGET_NAMES[x], self.TARGETS)

        # Header
        self.label("%s %s" % (self.my_name.upper(), self.my_version),
            bg=self.bg2, fg=self.fg2).grid(columnspan=2, ipadx=10)
        self.label("ONE source, MULTI targets" + '\n%s\n' % self.my_url,
            bg=self.bg1, fg=self.fg1).grid(columnspan=2)
        self.row = 2
        # Choose input file
        self.action(action1)
        self.frame_open()
        e_infile = self.entry(textvariable=self.infile, width=25)
        e_infile.grid(row=self.row, column=0, sticky='e')
        if not self.infile.get():
            e_infile.focus_set()
        self.button("Browse", self.askfile).grid(
            row=self.row, column=1, sticky='w', padx=10)
        # Show outfile name, style and encoding (if any)
        txt = ''
        if outfile:
            txt = outfile
            if outfile == STDOUT:
                txt = '<screen>'
            l_output = self.label('Output: ' + txt, fg=self.fg2, bg=self.bg2)
            l_output.grid(columnspan=2, sticky='w')
        for setting in ['style', 'encoding']:
            if self.conf.get(setting):
                name = setting.capitalize()
                val  = self.conf[setting]
                self.label('%s: %s' % (name, val),
                    fg=self.fg2, bg=self.bg2).grid(
                    columnspan=2, sticky='w')
        # Choose target
        self.frame_close()
        self.action(action2)
        self.frame_open()
        self.target_key2name()
        self.menu(self.target_name, targets_menu).grid(
            columnspan=2, sticky='w')
        # Options checkboxes label
        self.frame_close()
        self.action(action3)
        self.frame_open()
        # Compose options check boxes, example:
        # self.check(checks_txt['toc'], 1, variable=self.f_toc)
        for check in self.checks:
            # Extra options label
            if check == 'toc-only':
                self.frame_close()
                self.action(action4)
                self.frame_open()
            txt = checks_txt[check]
            var = getattr(self, 'f_' + check)
            checked = self.conf.get(check)
            self.check(txt, checked, variable=var)
        self.frame_close()
        # Spacer and buttons
        self.label('').grid()
        self.row += 1
        b_quit = self.button("Quit", self.exit)
        b_quit.grid(row=self.row, column=0, sticky='w', padx=30)
        b_conv = self.button("Convert!", self.runprogram)
        b_conv.grid(row=self.row, column=1, sticky='e', padx=30)
        if self.target.get() and self.infile.get():
            b_conv.focus_set()

        # As documentation told me
        if sys.platform.startswith('win'):
            self.root.iconify()
            self.root.update()
            self.root.deiconify()

        self.root.mainloop()


##############################################################################
