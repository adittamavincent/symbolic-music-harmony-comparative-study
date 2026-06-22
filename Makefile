-include .env.local
export

.PHONY: compile

compile:
	@if [ ! -f .env.local ]; then \
		echo "Warning: .env.local not found. Using empty environment variables."; \
	fi
	envsubst < thesis/main.tex.template > thesis/main.tex
	latexmk -pdf -cd -outdir=thesis thesis/main.tex

present:
	@if [ ! -f .env.local ]; then \
		echo "Warning: .env.local not found. Using empty environment variables."; \
	fi
	envsubst < thesis/presentation.tex.template > thesis/presentation.tex
	latexmk -pdf -cd -outdir=thesis thesis/presentation.tex
