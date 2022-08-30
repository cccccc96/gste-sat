// Ring buffer FIFO.
// tail points to the insertion point unless the buffer is full.
// head points to the first element in the queue unless the buffer is empty.
// A push on a full buffer is a NOOP.
// A pop from an empty buffer is a NOOP.
// If both push and pop are asserted at the same clock cycle, only the push
// operation is performed.
// dataOut gives the first element of the queue unless the buffer is empty,
// in which case its value is arbitrary.
module rbFIFO(rst,clock,dataIn,push,pop,dataOut,full,empty);
    parameter	    MSBD = 3;
    parameter	    LAST = 15;
    parameter	    MSBA = 3;
    input	    rst;
    input	    clock;
    input [MSBD:0]  dataIn;
    input	    push;
    input	    pop;
    output [MSBD:0] dataOut;
    output	    full;
    output	    empty;

    reg [MSBD:0] dataOut;
    reg [MSBD:0]    mem[0:LAST];
    reg [MSBA:0]    tail;
    reg [MSBA:0]    head;
    reg		    empty;
    integer	    i;

    initial begin
	for (i = 0; i <= LAST; i = i + 1)
	    mem[i] = 0;
	tail = 0;
	head = 0;
	empty = 1;
    end // initial begin

    always @ (posedge clock) begin
    if (rst) begin
            for (i = 0; i <= LAST; i = i + 1)
                mem[i] = 0;
            tail = 0;
            head = 0;
            empty = 1;
            full=0;
        end
	else if (push & ~full) begin
	    mem[tail] = dataIn;
	    tail = tail + 1;
	    empty = 0;
	end // if (push & ~full)
	else if (pop & ~empty) begin
	    head = head + 1;
	    if (head == tail)
		empty = 1;
	end // if (pop & ~empty)
	full = (head == tail) & ~empty;
	dataOut = mem[head];
    end // always @ (posedge clock)



endmodule // rbFIFO
