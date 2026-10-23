module instr_mem(input logic [15:0] addr, output logic [7:0] instr);

            logic [7:0] mem [0:65535];
            genvar i;
            generate
                 for (i = 0; i < 10; i = i + 1) begin : gen_mem_view
                wire [15:0] instr_mem = mem[i];
            end
            endgenerate


            always_comb begin
                    instr = mem[addr];
            end 


        

endmodule