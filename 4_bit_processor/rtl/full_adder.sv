module full_adder(input logic a,b,cin, output logic sum,cout);

        logic x;
        xor_gate xor_1(.a(a),.b(b),.y(x));
        xor_gate xor_2(.a(x),.b(cin),.y(sum));
        assign cout = (x & cin) | (a & b);


endmodule  
