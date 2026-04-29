MAIN = report

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex
	pdflatex $(MAIN).tex
	pdflatex $(MAIN).tex

.PHONY: clean
clean:
	rm -f *.aux *.log *.out *.toc $(MAIN).pdf

make file
