CC=go
Fbuild=build -o
Frun=run
Prog=tp4

all: $(Prog)

$(Prog): *.go
	$(CC) $(Fbuild) $(Prog) *.go

run: $(Prog)
	./$(Prog)

clean:
	rm $(Prog)
