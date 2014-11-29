#
# DEVELOPERS:
#
# This is the projects makefile
# It determines how source files get converted
# into an EPUB

# You can change this file to adjust the process
# and add new outputs.

DOCX=$(shell ls *.docx)
DOCX_MD = $(DOCX:%.docx=%.md)
scripts=/usr/lib/cgi-bin
sources=$(shell python $(scripts)/sources.py)

all: publication.epub publication.icml publication.gif

publication.epub: metadata.txt publication.md styles.css
	pandoc metadata.txt publication.md \
	--table-of-contents \
	--epub-stylesheet styles.css \
	-o publication.epub

publication.icml: publication.md styles.css
	pandoc publication.md --to ICML -o publication.icml

# Concatenate all Markdown sources into a single file
# Adding the filename as a unique identifier for footnotes
#publication.md: $(sources)
#	cat $(sources) > publication.md

publication.gif: publication.epub styles.css
	python $(scripts)/epubtrailer.py $< --background "#EEEEEE" --width 320 --height 240 --duration=0.5 -o $@

publication.md: metadata.txt $(sources) $(DOCX_MD)
	rm -f $@
	cat metadata.txt > $@
	$(foreach c,$(sources),pandoc --to markdown --id-prefix=$(c) $(c) >> $@; echo >> $@; echo >> $@;)
	echo "The End" >> $@

	# cat metadata.txt >> $@
	# $(scripts)/expand_toc.py toc.md --filter $(scripts)/chapter.sh | \
	# python $(scripts)/enable_links_markdown.py >> $@

# MARKDOWN <= DOCX
%.md: %.docx
	pandoc $< -o $@

# special rule for debugging variable names in this makefile
print-%:
	@echo '$*=$($*)'
