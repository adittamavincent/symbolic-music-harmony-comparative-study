-include .env.local
export

.PHONY: compile

all: compile present notes

compile:
	@if [ ! -f .env.local ]; then \
		echo "Warning: .env.local not found. Using empty environment variables."; \
	fi
	envsubst < thesis/proposal/main.tex.template > thesis/proposal/main.tex
	TEXINPUTS=.:../assets: latexmk -pdf -cd -auxdir=build -outdir=. thesis/proposal/main.tex

present:
	@if [ ! -f .env.local ]; then \
		echo "Warning: .env.local not found. Using empty environment variables."; \
	fi
	envsubst < thesis/slides/presentation.tex.template > thesis/slides/presentation.tex
	TEXINPUTS=.:../assets: latexmk -pdf -cd -auxdir=build -outdir=. thesis/slides/presentation.tex

notes:
	@if [ ! -f .env.local ]; then \
		echo "Warning: .env.local not found. Using empty environment variables."; \
	fi
	envsubst < thesis/slides/presentation_notes.tex.template > thesis/slides/presentation_notes.tex
	TEXINPUTS=.:../assets: latexmk -pdf -cd -auxdir=build -outdir=. thesis/slides/presentation_notes.tex

clean:
	rm -rf thesis/proposal/build thesis/slides/build
	rm -f thesis/proposal/*.tex thesis/slides/*.tex
