module xor_gate(input logic a,input logic b, output logic y);

            always_comb begin : XOR_BEHAVIOURAL_MODEL

                    if(a==b)
                         y  = 0;
                    else
                         y = 1;

            end

endmodule 

