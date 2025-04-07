FROM ollama/ollama
COPY Modelfile /Modelfile
RUN ollama create phi3-custom -f /Modelfile && ollama serve
CMD ["ollama", "serve"]
