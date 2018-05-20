PROJECT = ${name}
OBJECTS = ${name}.o

CFLAGS = -std=c11 -Wall
LDFLAGS =

$(PROJECT): $(OBJECTS)
	gcc $(CFLAGS) -o $@ $^ $(LDFLAGS)

%%.o: %.c
	gcc $(CFLAGS) -c $<

clean:
	rm -f $(PROJECT) $(OBJECTS)

.PHONY: clean
