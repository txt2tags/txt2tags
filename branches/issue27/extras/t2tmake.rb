#!/usr/bin/env ruby

require 'optparse'
require 'fileutils'

=begin
:title: Documentação do t2t-make

 = t2tmake.rb (0.8beta)
 Programa para o processamento automatico de arquivos utilizando
 o txt2tags <t2t> (http://txt2tags.org)
 
 == download e instalação
 Existem duas maneiras de baixar este programa:
 - Na área de arquivos da lista[http://groups.yahoo.com/group/txt2tags-br].
   dos usuários do txt2tags (em português)
 - Na página[http://txt2tags-win.sourceforge.net/t2tmake.zip] em português do txt2tags.

 ===requisitos
 - txt2tags (é claro, sem ele este programa não existiria);
 - ruby 1.6.8+ (é lógico, senão este programa não roda);
 - python 1.5+ (sim, sim, para o txt2tags rodar);
 
 ===instalação: (t2t)
 - txt2tags: verifique o site http://txt2tags.org;
 - python: verifique o site www.python.org;
 
 ===instalação (ruby)
 - Windows:
   Baixe de http://rubyinstaller.sourceforge.net e execute o
   programa de instalação.
 - Linux:
   A maioria das grandes distribuições já possuem o pacote em
   algum CD. Siga os procedimentos normais de instalação. Caso
   não exista para a sua, baixe os fontes de
   http://www.ruby-lang.org/en/ e siga os procedimentos.
 - Mac OSX:
   As versões atuais já trazem o Ruby. Caso contrário seria
   necessário baixar os fontes de http://www.ruby-lang.org/en/
   e compilar.
 - Cygwin:
   Rode o programa de setup, e instale a versão compilada do
   Ruby (1.6.8).
 - Outros:
   Não tenho idéia. Só vendo.
 
 ===instalação (programa)
 - apenas copie o programa para o local de sua preferência (em
   um local onde ele possa ser executado sem especificar o
   caminho é uma boa idéia)
 
 ==características
 - processa apenas os arquivos necessários (atualizados ou inexistentes);
 - permite o processamento recursivo (subdiretórios);
 - gera log dos arquivos para facilitar a atualização de sites;
 - roda em Windows, Linux, Cygwin, (etc?)
 - opção para adequação de indexes localizados para o Apache,
   index-ptbr.t2t => index.html.ptbr
 - aceita opções a partir de um arquivo de configuração (+veja observações abaixo+)
 - permite listar os rótulos existentes no arquivo de configuração  

 ===Obs: 
 ==== --batch filename rótulo
 - deve ser a última opção da linha de comando
 - as opções anteriores mantidas são: --clean --all
 - o arquivo contendo as opções é um arquivo texto no seguinte formato:
 - os rótulos devem estar entre chaves
 - deixar uma linha em branco para separar os rótulos
 - caminhos contendo espaçoes deverão estar entre aspas "caminho"
	[rotulo]
	--opção
	...
	--opção
 ex.:

 [txt2tags-win]
 --L10N
 --type html
 --sdir "C:/Arquivos de programas/Apache Group/Apache/htdocs/txt2tags-win"
 --ddir "C:/Arquivos de programas/Apache Group/Apache/htdocs/txt2tags-win"
 -r


 ==por fazer:
 - inclusão de opções de pesquisa (--todo e --find text|ER)
 - inclusão de opções de alteração (--subs texto:texto)
 - aceitar outras opções para enviar ao t2t
 - ??
 
 = copyright
 (C) 2003 por Guaracy Monteiro (http://ruby-ptbr.rubyforge.org/)
 
 = licenças
 GPL + Ruby (ou seja, faça o uso que desejar)
 
 = historico
 [A]lteração; Correção de [B]ugs; [N]ovo

 25/08/2003
 - lançamento (testes iniciais no Mandrake 9.1 e Windows 2000 utilizando
   ruby 1.8 e no Cygwin utilizando ruby 1.6.8)
 30/08/2003
 - [A]alterações nos comentários do programa para a geração automática 
   da documentação pelo rdoc;
 - [A]alterações em nomes de variáveis e métodos do programa
   bem como de opções aceitas pelo mesmos e respectivas rotinas;
 - [B]passagem de diretório com espaços para o txt2tags;
 - [N]opção L10N para arquivos de indices do Apache. Executada
   apenas para --type html
   index-en.t2t, index-ptbr.t2t => index.html.en, index.html.ptbr;
 - [N]opção --batch filename label. Abre um arquivo de configuração
   (default => t2t-make.conf), procura pelo rótulo especificado e
   passa para a linha de comandos as opções encontradas no arquivo
   (encerra na primeira linha em branco);
 - [N]opção -L. Utilizada em conjunto com a opção --batch e serve
   para apenas listar os rótulos encontrados no arquivo sem a
   execução do mesmo;
 - [A]separação da rotina para interpretar a linha de comandos
   para facilitar a execução de arquivos de lotes;
 - [N]opção --ext extensão para gerar arquivo com extensão
   diferente da padrão;
 - [N]opção --all para forçar a atualização de todos os arquivos
 09/07/2004
 - [A]correções diversas para atualização
 10/07/2004
 - [A]utilização de optparse para verificação das opções
 - [A]exclusão do parâmetro -L
 - [N]parâmetro -b/--batch lista rótulo em caso de omissão ou erro
 - [A]alteração dos métodos para tratamento de arquivos batch
 - [N]lançamento da versão 1.0rc
 - [A]exclusão do método usage (incorporado na verificação dos parâmetros)
 - [A]alterações em diversas partes do programa por conta da 'optparse'
 - [N]é salvo a data e os dados são adicionados no logfile
=end

# versão do programa
$VERSAO = "1.0rc"

#++ >> ATENÇÃO <<
# A constante $T2T contém o caminho para o txt2tags e
# deve ser alterada conforme o seu sistema
# Alguns exemplos:
# $T2T = 'python C:/utils/txt2tags.py'
# $T2T = 'E:/utils/txt2tags/txt2tags.exe'
# $T2T = /usr/local/bin/txt2tags

if RUBY_PLATFORM =~ /mswin/
  $T2T = 'C:/Arquivos de programas/txt2tags/txt2tags.exe'
  $POPEN = true
else
  $T2T = 'txt2tags'
  $POPEN = true #false
end

$flags = ''

$IDX_SRC = 0		# indice para caminho dos fontes
$IDX_DSTDIR = 1		# indice para caminho dos destinos
$IDX_DSTFILE = 2	# indice para nome do arquivo destino


# Tipos válidos para o txt2tags
$tipos = %w(html xhtml sgml tex man mgp moin pm6 txt)

# Mostra uma mensagem de erro e aborta o programa
# ---
def abort(msg)
  puts "Abnormal program termination!"
  puts msg
  exit
end

# Retorna uma string com a versão do programa
# ---
def version
  print "\nt2tmake.rb version #{$VERSAO}\n"
  print "(c) 2003 by Guaracy B. Monteiro\n\n"
end


# Pesquisa um diretório e executa um bloco passado para
# cada arquivo que coincidir com a máscara especificada
# Se _recursive_ for igual a +verdadeiro+, a pesquisa
# será efetuada em toda a árvore do diretório informado
#---
def dir_recurse(dirname, mask, recursive, &action)
  d = Dir.pwd
  Dir.chdir(dirname)
  Dir["#{mask}"].each do |file|
    action.call("#{dirname}/#{file}")
  end
  return if !recursive
  Dir.open(dirname) do |dir|
    dir.each do |file|
      if FileTest.directory?("#{dirname}/#{file}")
        next if file =~ /^\.\.?$/
        dir_recurse("#{dirname}/#{file}", mask, recursive, &action)
      end
    end
  end
  Dir.chdir(d)
end

# Recebe uma matriz com o caminho completo e nome dos 
# arquivos, a especificação do diretório original, a 
# especificação do diretório destino e o tipo (extensão) 
# dos arquivos destinos.
# Retorna uma matriz onde cada elemento contém:
# - caminho completo e nome dos arquivos de origem
# - caminho completo do destino
# - nome e extensão do arquivo destino correspondente
# ---
def gen_destfiles(files, srcdir, dst_dir, type)
  basedir = srcdir.size
  files.collect do |filedir|
    dir = dst_dir + File.dirname(filedir)[basedir..-1]
    file = File.basename(filedir,'.t2t')
    if !@l10n.nil?
      if type == 'html' and file =~ /^index\-/
        file = file.split('-',2)
        file = sprintf("%s.%s.%s", file[0] , type, file[1])
      else
        file << ".#{type}"
      end
    else
      file << ".#{type}"
    end
    [filedir, dir, file]
  end
end

# Rotina para a verificar se o arquivo fonte é mais
# atual que o arquivo destino ou se este não existe.
# Se for confirmada a condição, o programa executará
# o txt2tags para que a atualização do destino seja
# feita, bem como irá gravar no arquivo +logfile+ o
# caminho completo e nome do arquivo destino que
# foi alterado.
# ---
def make(files, logfile)
  if !@log_fn.nil?
		logfile = File.new(logfile,"a") 
		logfile.puts Time.new.strftime("# %c\n")
	end
  files.each do |data|
    src = data[$IDX_SRC]
    dstdir = data[$IDX_DSTDIR]
    dst = "#{dstdir}/#{data[$IDX_DSTFILE]}"
    begin
      if !FileTest.exist?(dstdir)
			  FileUtils.mkdir_p(dstdir)
      end
    rescue => erro
      abort("Can't create directory - #{dstdir}")
    end
    if !@all.nil? or !File.exist?(dst) or File.stat(src).mtime > File.stat(dst).mtime
      puts "Processing - #{src}"
      cmd = "\"#{$T2T}\" #{$flags} -o \"#{dst}\" \"#{src}\""
      if $POPEN
        IO.popen(cmd) { |res|
          puts res.readlines
        }
      else
        if !system(cmd)
          abort("Error while executin - '#{$T2T}'")
        end
      end
      logfile.puts dst if !@log_fn.nil?
    else
      puts"Nothing to be done for - #{data[$IDX_DSTFILE]} #{src}"
    end
  end
end

# Remove todos os arquivos com uma determinada
# extensão em um diretório destino baseado em
# uma lista de arquivos fontes especificadas
# ---
def clean(files, type, dst_dir)
  puts "Cleaning..."
  files.each do |data|
    dst = "#{data[$IDX_DSTDIR]}/#{data[$IDX_DSTFILE]}"
    if File.exist?(dst)
      puts "deleting - #{dst}"
      File.delete(dst)
    end
  end
end

# Mostra rótulos válidos em arquivo batch e encerra
# ---
def abort_batch_labels(conf_file, data, msg)
    puts msg unless msg.empty?
    puts "Valid labels for #{conf_file}:"
    data.each do |line|
      puts "#{line}" if line =~ /^\[.+\]\s*/ 
    end
    exit
end

# Pocessamento de arquivos com instruções
# ---
def batch(file,label,msg="")
  conf_file = File.expand_path(file)
  conf_file += "/t2t-make.conf" if FileTest.directory?(conf_file)
  if !FileTest.exist?(conf_file)
    puts "Can't find file #{conf_file}"
    exit
  end
  data = IO.readlines(conf_file)
  data.collect! do |linha| linha.chop end
  if label.nil?
    abort_batch_labels(conf_file,data,msg)
  end
  idx = data.index("[#{label}]")
  if idx.nil?
    abort_batch_labels(conf_file,data,"Can't find label - '#{label}'")
  end
  for i in (idx+1)..(data.size-1)
    break if data[i] == ''
    abort("Malformated line\nfile : #{conf_file}\nlabel : [#{label}]\nline -  #{data[i]}\nin") if data[i] !~ /^\-/
      ARGV << data[i].split(nil,2)
  end
  ARGV.flatten!
end

# Rotina principal do programa, encarregada de verificar
# os argumentos especificados na linha de comando.
# ---
def parse_args
    ARGV.options do
      |opts|
      opts.on_tail
      opts.on_tail("common options:")
      opts.on_tail("-h", "--help", "show this message") do
        puts opts
        exit
      end
      opts.on_tail("-V", "--version", "show version") do
        puts "t2tmake #{$VERSION}"
        exit
      end
      opts.on_head("specific options:")  
      opts.on("-t", "--type=TARGET", String, "set target (txt2tags) document type",$tipos.join(",")) do |x|@type=x
        if !@type.nil?
          if !$tipos.include?(@type)
            puts "'#{@type}' is not a valid target type. Valid types are:"
            puts $tipos.join(' | ')
            exit
          end
        end
      end
      # formal argument cannot be an instance variable: {|@ext|}
      opts.on("-e", "--ext=EXT", String, "set output file extension") {|x|@ext=x}
      opts.on("-r", "--recusive", "recursive directory processing.") {|x|@recursive=x}
      opts.on("-s", "--sdir=DIR", String, "especify source directory","default => actual_directory (pwd)") {|x|@src_dir=x}
      opts.on("-d", "--ddir=DIR", String, "set target directory","default => actual_directory./_<type>") {|x|@dst_dir=x}
      opts.on("-l", "--log[=FILE]", "log changes (processed files)","default => target_directory/t2tmake.log") {|x|@log_fn=x;@log_fn ||= ''}
      opts.on("--L10N", "Apache localization", "index-en.t2t => index.html.en") {|x|@l10n=x}
      opts.on("-a", "--all", "force to process all files") {|x|@all=x}
      opts.on("-c", "--clean", "erase all target files before processing") {|x|@clean=x}
      opts.on("-b", "--batch=FILE[,LABEL]",Array,"use options from an specified 'label'","stored in a batch file;","without LABEL, list all labels") do |x,y|@batch,@label=x,y
        if @label.nil?
          batch(@batch,@label,"No label specified.")
          exit
        end
      end
      opts.parse!
    end
end

# Verificar a validade dos argumentos passados para o programa
# e toma as providencias necessárias como ajustar nomes de 
# diretórios, montar a lista de arquivos e chamar o método 
# responsável para execução dos procedimentos desejados pelo 
# usuário.
# ---
def main
  # warning: instance variable @foo not initialized
  @batch = nil
  @type = nil
  @src_dir = nil
  @dst_dir = nil
  @ext = nil
  @recursive = nil
  @clean = nil
  @log_fn = nil
  @log_fn = nil

#  if ARGV.empty?
#    ARGV.push("--help")
#  end
  fbatch = false
  while true do
    parse_args
    if !@batch.nil?
      abort("Nested batch files not allowed.") if fbatch
      ARGV.clear
      batch(@batch,@label)
      @batch=nil
      fbatch = true
      next
    else
      break
    end
  end
	
	@type='html' if @type.nil?
	
  if @src_dir.nil?
    src_dir = Dir.pwd
  else
    src_dir = @src_dir.gsub(/[\"\']/,'')
    src_dir = File.expand_path(src_dir)
  end
	
  if @dst_dir.nil?
    dst_dir = src_dir + "/_#{@type}"
  else
    dst_dir = @dst_dir.gsub(/[\"\']/,'')
    dst_dir = File.expand_path(dst_dir)
  end
  if !FileTest.exist?(dst_dir)
		FileUtils.mkdir_p(dst_dir)
  end

  files = []	
	
  ext = (@ext.nil?) ? (@type) : (@ext)
  dir_recurse(src_dir, "*.t2t", !@recursive.nil?) { |file| files << file }
  files = gen_destfiles(files, src_dir, dst_dir, ext)
  if !@clean.nil?
    clean(files, type, dst_dir)
    return
  end
	if !@log_fn.nil?
		logfile = (@log_fn.empty?) ? ("#{dst_dir}/t2tmake.log") : (File.expand_path(@log_fn))
		if !FileTest.exist?(File.dirname(logfile))
			begin
				Dir.mkdir("#{File.dirname(logfile)}")
			rescue => erro
				abort("#{erro}\nCan't create logfile - #{logfile}")
			end
		end
	else
		logfile = ""
	end

  make(files, "#{logfile}")
	
end


=begin

  #clean não usa log
  $flags = $flags + "-t #{$OPT_type} "
  end
=end

# inicio do programa
main
puts "Done."

