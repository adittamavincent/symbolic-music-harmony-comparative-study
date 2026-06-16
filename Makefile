-include .env.local
export

.PHONY: compile

compile:
	@if [ ! -f .env.local ]; then \
		echo "Warning: .env.local not found. Using empty environment variables."; \
	fi
	envsubst < thesis/main.tex.template > thesis/main.tex
	latexmk -pdf -cd -outdir=thesis thesis/main.tex
